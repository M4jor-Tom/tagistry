from pydantic import BaseModel


class TagJsonModel(BaseModel):
    category: str
    value: str
    parent_tags_names: list[str]
