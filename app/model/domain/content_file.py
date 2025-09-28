from __future__ import annotations

from pydantic import BaseModel
from loguru import logger

from exception import TagsFileNamePartNotFound


class ContentFile(BaseModel):
    path: str
    content_hash: str | None

    @staticmethod
    def sanitize_tags(file_name: str) -> list[str]:
        file_name_split: list[str] = file_name.split(" ")
        if len(file_name_split) < 1:
            raise TagsFileNamePartNotFound()
        tags_part: str = file_name_split[0]
        if "{" not in tags_part and "}" not in tags_part:
            raise TagsFileNamePartNotFound()
        tags: list[str] = tags_part.lstrip("{").rstrip("}").split("}{")
        return tags

    @staticmethod
    def build_content_file(path: str, content_hash: str | None) -> ContentFile:
        path_split: list[str] = path.split('/')
        base_name: str = path_split[-1] if len(path_split) > 1 else path
        logger.debug(ContentFile.sanitize_tags(base_name))
        return ContentFile(path=path, content_hash=content_hash)
