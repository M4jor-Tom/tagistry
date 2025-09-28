import hashlib
from pathlib import Path

from loguru import logger

from exception import TagsSanitizingException, TagsFileNamePartNotFound
from model.domain import ContentFile


class ContentFileService:
    content_files: list[ContentFile]
    found_tags: set[str]

    def __init__(self):
        self.content_files = []
        self.found_tags = set()

    def sanitize_tags(self, file_name: str) -> list[str]:
        file_name_split: list[str] = file_name.split(" ")
        if len(file_name_split) < 1:
            raise TagsFileNamePartNotFound()
        tags_part: str = file_name_split[0]
        if "{" not in tags_part and "}" not in tags_part:
            raise TagsFileNamePartNotFound()
        tags: list[str] = tags_part.lstrip("{").rstrip("}").split("}{")
        for tag in tags:
            self.found_tags.add(tag)
        return tags

    def build_content_file(self, path: str, content_hash: str | None) -> ContentFile:
        path_split: list[str] = path.split('/')
        base_name: str = path_split[-1] if len(path_split) > 1 else path
        logger.debug(self.sanitize_tags(base_name))
        return ContentFile(path=path, content_hash=content_hash)

    @staticmethod
    def is_path_to_take(path: Path, banned_strips: tuple[str, ...]) -> bool:
        for blacklisted in banned_strips:
            if blacklisted in str(path):
                return False
        return path.is_file()

    @staticmethod
    def file_sha256(path: Path) -> str:
        sha256 = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def input_content_file(
            self,
            stripped_str_content_file: str,
            content_file_path_object: Path,
            compute_hash: bool
    ) -> None:
        self.content_files.append(self.build_content_file(
            path=stripped_str_content_file,
            content_hash=ContentFileService.file_sha256(content_file_path_object) if compute_hash else None
        ))

    def input_content_files(self,
                            content_file_absolute_parent_dir: str,
                            banned_strips: tuple[str, ...],
                            compute_hash: bool
                            ):
        for path in Path(content_file_absolute_parent_dir).rglob("*"):
            try:
                if ContentFileService.is_path_to_take(path, banned_strips):
                    relative_file_split: list[str] = str(path).split(content_file_absolute_parent_dir)
                    if len(relative_file_split) == 2:
                        relative_path: str = relative_file_split[1]
                        self.input_content_file(relative_path.lstrip('/'), path, compute_hash)
            except TagsSanitizingException as e:
                logger.error(f"Refused path {str(path)} for {e.reason}")
        logger.debug("found_tags: {}", self.found_tags)
