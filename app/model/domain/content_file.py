from __future__ import annotations

from pydantic import BaseModel
from loguru import logger

from exception import TagsFileNamePartNotFound


class ContentFile(BaseModel):
    path: str
    content_hash: str | None
