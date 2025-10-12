from __future__ import annotations

from pydantic import BaseModel

from model.persistence import TagJsonObject


class Tag(BaseModel):
    category: str
    value: str
    parent_tags: list[Tag]

    def inherits_of(self, tag: Tag) -> bool:
        if tag.value in [parent_tag.value for parent_tag in self.parent_tags]:
            return True
        for parent_tag in self.parent_tags:
            if parent_tag.inherits_of(tag):
                return True
        return False

    def to_file_json(self) -> TagJsonObject:
        return TagJsonObject(
            category=self.category,
            value=self.value,
            parent_tags_names=[parent_tag.value for parent_tag in self.parent_tags]
        )
