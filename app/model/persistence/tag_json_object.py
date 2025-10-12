from pydantic import BaseModel


class TagJsonObject(BaseModel):
    category: str
    value: str
    parent_tags_names: list[str]

    def __hash__(self):
        return hash((self.category, self.value, tuple(self.parent_tags_names)))
