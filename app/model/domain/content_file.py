from __future__ import annotations

from pydantic import BaseModel


class ContentFile(BaseModel):
    path: str
    content_hash: str | None
    tag_values: list[str]
    missing_tag_values: list[str]
