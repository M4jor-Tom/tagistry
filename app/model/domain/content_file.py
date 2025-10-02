from __future__ import annotations

from pydantic import BaseModel


class ContentFile(BaseModel):
    dir_name: str
    base_name_without_extension: str
    extension: str
    content_hash: str | None
    tag_values: list[str]
    missing_tag_values: list[str]

    @property
    def path(self) -> str:
        base_name: str = f"{self.base_name_without_extension}.{self.extension}"\
            if self.extension != ""\
            else self.base_name_without_extension
        if self.dir_name != "" and base_name != "":
            return f"{self.dir_name}/{base_name}"
        return base_name
