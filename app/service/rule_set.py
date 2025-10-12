from functools import cache
from pathlib import Path

from loguru import logger

from exception import RuleSetElementPathDoesNotExist, InconsistentRuleSetCategoryInheritanceException, \
    RuleSetImportException, InheritanceTagsAbsentFromCategoriesTagsException, TagJsonObjectInheritsFromNonExistentTag
from model.domain import Tag
from model.persistence import TagJsonObject


class RuleSetService:
    tags: dict[str, Tag]
    tag_file_exceptions: list[RuleSetImportException] = []

    def __init__(self):
        self.tags = {}

    @staticmethod
    def build_rule_set_element_from_dir(rule_set_element_dir: str, banned_strips: tuple[str, ...]) -> dict[
        str, list[str]]:
        rule_set_element: dict[str, list[str]] = {}
        if not Path(rule_set_element_dir).exists():
            raise RuleSetElementPathDoesNotExist(value=rule_set_element_dir)
        rule_set_element_sub_dirs: list[str] = [
            rule_set_sub_dir.name for rule_set_sub_dir in Path(rule_set_element_dir).iterdir()]
        for rule_set_element_file_name in rule_set_element_sub_dirs:
            if rule_set_element_file_name not in banned_strips:
                rule_set_sub_element_value: list[str] = (Path(f"{rule_set_element_dir}/{rule_set_element_file_name}")
                                                         .read_text(encoding="utf-8").split())
                rule_set_element[Path(rule_set_element_file_name).stem] = rule_set_sub_element_value
        return rule_set_element

    @staticmethod
    def build_tags_from_tags_categories(tags: dict[str, Tag], tags_categories: dict[str, list[str]]) -> dict[str, Tag]:
        for tag_category in tags_categories:
            for tag_value in tags_categories[tag_category]:
                tags[tag_value] = Tag(
                    category=tag_category,
                    value=tag_value,
                    parent_tags=[]
                )
        return tags

    @staticmethod
    def sanitize_and_update_tags_from_tags_inheritances(
            tags: dict[str, Tag], tags_inheritance: dict[str, list[str]]) -> dict[str, Tag]:
        absent_son_category_tags_from_inheritance_tags: set[str] = set[str]()
        for parent_tag_value in tags_inheritance:
            for son_tag_value in tags_inheritance[parent_tag_value]:
                if son_tag_value not in tags:
                    absent_son_category_tags_from_inheritance_tags.add(son_tag_value)
                elif parent_tag_value in tags:
                    tags[son_tag_value].parent_tags.append(tags[parent_tag_value])
        if len(absent_son_category_tags_from_inheritance_tags) > 0:
            raise InheritanceTagsAbsentFromCategoriesTagsException(f"{absent_son_category_tags_from_inheritance_tags}")
        return tags

    @staticmethod
    def sanitize_ruleset_consistency(tags: dict[str, Tag], categories_inheritance: dict[str, list[str]]) -> None:
        inconsistent_tags_with_intended_category: list[tuple[str, list[str]]] = []
        for tag in tags.values():
            any_parent_tag_has_right_category: bool = False
            tag_category_should_have_parents: bool = tag.category in categories_inheritance
            if tag_category_should_have_parents:
                tag_parent_categories: list[str] = [parent_tag.category for parent_tag in tag.parent_tags]
                for tag_parent_category in tag_parent_categories:
                    parent_tag_has_right_category: bool = tag_parent_category in categories_inheritance[tag.category]
                    any_parent_tag_has_right_category = parent_tag_has_right_category or \
                                                        any_parent_tag_has_right_category
                if not any_parent_tag_has_right_category:
                    inconsistent_tags_with_intended_category.append(
                        tuple[str, list[str]]([tag.value, categories_inheritance[tag.category]]))
        if len(inconsistent_tags_with_intended_category) > 0:
            raise InconsistentRuleSetCategoryInheritanceException(inconsistent_tags_with_intended_category)

    @staticmethod
    def build_tags_from_dir(rule_set_dir: str, banned_strips: tuple[str, ...]) -> dict[str, Tag]:
        tags: dict[str, Tag] = {}
        tags_categories: dict[str, list[str]] = RuleSetService.build_rule_set_element_from_dir(
            f"{rule_set_dir}/tags-categories",
            banned_strips)
        tags_inheritance: dict[str, list[str]] = RuleSetService.build_rule_set_element_from_dir(
            f"{rule_set_dir}/tags-inheritance",
            banned_strips)
        categories_inheritance: dict[str, list[str]] = RuleSetService.build_rule_set_element_from_dir(
            f"{rule_set_dir}/categories-inheritance",
            banned_strips)
        tags = RuleSetService.build_tags_from_tags_categories(tags, tags_categories)
        tags = RuleSetService.sanitize_and_update_tags_from_tags_inheritances(tags, tags_inheritance)
        RuleSetService.sanitize_ruleset_consistency(tags, categories_inheritance)
        return tags

    def import_rule_set(self, rule_set_dir: str, banned_strips: tuple[str, ...]) -> None:
        try:
            self.get_tags_values.cache_clear()
            self.tags = RuleSetService.build_tags_from_dir(rule_set_dir, banned_strips)
        except RuleSetImportException as e:
            logger.warning(e.get_details())

    def build_tag_from_tags_json_objects(self, tag: TagJsonObject, tags: dict[str, TagJsonObject]) -> Tag:
        if tag.value in self.tags:
            return self.tags[tag.value]
        for parent_tag_name in tag.parent_tags_names:
            if parent_tag_name not in tags:
                self.tag_file_exceptions.append(TagJsonObjectInheritsFromNonExistentTag(
                    non_existent_parent_tag_value=parent_tag_name, tag_value_with_parent_error=tag.value))
        new_tag: Tag = Tag(
            value=tag.value,
            category=tag.category,
            parent_tags=[self.build_tag_from_tags_json_objects(tags[parent_tag_name], tags) for
                         parent_tag_name in tag.parent_tags_names if parent_tag_name in tags]
        )
        self.tags[tag.value] = new_tag
        return new_tag

    def build_tags_from_tags_json_objects(self, tags: list[TagJsonObject]) -> list[Tag]:
        result: list[Tag] = []
        for tag_json_object in tags:
            result.append(self.build_tag_from_tags_json_objects(tag_json_object, {tag.value: tag for tag in tags}))
        return result

    def import_rule_set_by_tags(self, rule_set_file_content: str) -> dict[str, Tag]:
        self.tags = {}
        self.tag_file_exceptions = []
        tags: list[TagJsonObject] = [TagJsonObject.model_validate(item) for item in rule_set_file_content]
        self.tags = {tag.value: tag for tag in self.build_tags_from_tags_json_objects(tags)}
        for tag_file_exception in self.tag_file_exceptions:
            logger.warning(tag_file_exception.get_details())
        return self.tags

    @cache
    def get_tags_values(self) -> list[str]:
        return [rule_set_tag.value for rule_set_tag in self.tags.values()]
