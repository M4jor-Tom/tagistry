from pathlib import Path

from loguru import logger

from exception import RuleSetElementPathDoesNotExist, InconsistentRuleSetException, RuleSetImportException
from model.domain import Tag


class RuleSetService:
    tags: list[Tag]

    def __init__(self):
        self.tags = []

    @staticmethod
    def build_rule_set_element_from_dir(rule_set_element_dir: str, banned_strips: tuple[str, ...]) -> dict[
        str, list[str]]:
        rule_set_element: dict[str, list[str]] = {}
        if not Path(rule_set_element_dir).exists():
            raise RuleSetElementPathDoesNotExist(path=rule_set_element_dir)
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
    def update_tags_from_tags_inheritances(tags: dict[str, Tag], tags_inheritance: dict[str, list[str]]) -> dict[
        str, Tag]:
        for father_tag_value in tags_inheritance:
            for son_tag_value in tags_inheritance[father_tag_value]:
                tags[son_tag_value].parent_tags.append(tags[father_tag_value])
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
            raise InconsistentRuleSetException(inconsistent_tags_with_intended_category)

    @staticmethod
    def build_tags_from_dir(rule_set_dir: str, banned_strips: tuple[str, ...]) -> list[Tag]:
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
        tags = RuleSetService.update_tags_from_tags_inheritances(tags, tags_inheritance)
        RuleSetService.sanitize_ruleset_consistency(tags, categories_inheritance)
        return list(tags.values())

    def import_rule_set(self, rule_set_dir: str, banned_strips: tuple[str, ...]) -> None:
        try:
            self.tags = RuleSetService.build_tags_from_dir(rule_set_dir, banned_strips)
        except RuleSetImportException as e:
            logger.warning(e.get_details())

    def get_tags_values(self) -> list[str]:
        return [rule_set_tag.value for rule_set_tag in self.tags]
