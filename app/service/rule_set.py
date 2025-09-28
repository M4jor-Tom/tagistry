from pathlib import Path

from exception import RuleSetElementPathDoesNotExist
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
    def build_tags_from_dir(rule_set_dir: str, banned_strips: tuple[str, ...]) -> list[Tag]:
        tags: list[Tag] = []
        tags_categories: dict[str, list[str]] = RuleSetService.build_rule_set_element_from_dir(
            f"{rule_set_dir}/tags-categories",
            banned_strips)
        for tag_category in tags_categories:
            for tag_value in tags_categories[tag_category]:
                tags.append(Tag(
                    category=tag_category,
                    value=tag_value,
                    parent_tags=[]
                ))
        return tags

    def import_rule_set(self, rule_set_dir: str, banned_strips: tuple[str, ...]) -> None:
        self.tags = RuleSetService.build_tags_from_dir(rule_set_dir, banned_strips)
