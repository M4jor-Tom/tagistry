import hashlib
import re
from pathlib import Path

from loguru import logger

from exception import ContentImportException, FileNameWithoutSpacesException, UntaggedContentFileException, \
    TagNotAllowedException
from model.domain import ContentFile, ContentValidationSummary
from service import RuleSetService


class ContentFileService:
    content_files: list[ContentFile]
    all_found_tags: set[str]
    exceptions_summary: dict[type[ContentImportException], list[ContentImportException]]
    rule_set_service: RuleSetService

    def __init__(self, rule_set_service: RuleSetService):
        self.content_files = []
        self.all_found_tags = set()
        self.exceptions_summary = {}
        self.rule_set_service = rule_set_service

    def handle_content_import_exception(self, exception: ContentImportException):
        exception_type: type[ContentImportException] = type(exception)
        if exception_type not in self.exceptions_summary:
            self.exceptions_summary[exception_type] = []
        self.exceptions_summary[exception_type].append(exception)

    def sanitize_tags(self, path: str, file_name: str) -> list[str]:
        file_name_split: list[str] = file_name.split(" ")
        if len(file_name_split) < 1:
            raise FileNameWithoutSpacesException(path)
        tags_part: str = file_name_split[0]
        tags: list[str] = re.findall(r"{(\w+)}+", tags_part)
        if len(tags) == 0:
            raise UntaggedContentFileException(path)
        for tag in tags:
            self.all_found_tags.add(tag)
        return tags

    def sanitize_all_content_files_tags(self) -> tuple[list[str], list[TagNotAllowedException]]:
        allowed_tags: list[str] = []
        tag_not_allowed_exceptions: list[TagNotAllowedException] = []
        for found_tag in self.all_found_tags:
            if found_tag in self.rule_set_service.get_tags_values():
                allowed_tags.append(found_tag)
            else:
                tag_not_allowed_exceptions.append(TagNotAllowedException(found_tag))
        return allowed_tags, tag_not_allowed_exceptions

    def build_content_file(self, path: str, content_hash: str | None) -> ContentFile:
        path_split: list[str] = path.split('/')
        base_name: str = path_split[-1] if len(path_split) > 1 else path
        self.sanitize_tags(path, base_name)
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
                            ) -> ContentValidationSummary:
        for path in Path(content_file_absolute_parent_dir).rglob("*"):
            try:
                if ContentFileService.is_path_to_take(path, banned_strips):
                    relative_file_split: list[str] = str(path).split(content_file_absolute_parent_dir)
                    if len(relative_file_split) == 2:
                        relative_path: str = relative_file_split[1]
                        self.input_content_file(relative_path.lstrip('/'), path, compute_hash)
            except ContentImportException as e:
                self.handle_content_import_exception(e)

        allowed_tags, tag_not_allowed_exceptions = self.sanitize_all_content_files_tags()

        for tag_not_allowed_exception in tag_not_allowed_exceptions:
            self.handle_content_import_exception(tag_not_allowed_exception)

        for exception_type in self.exceptions_summary:
            occurrences_list: list[ContentImportException] = self.exceptions_summary[exception_type]
            logger.error("Refused {} paths for {}", len(occurrences_list), exception_type.reason)
            for exception in occurrences_list:
                logger.warning(exception.get_details())

        exceptions: list[ContentImportException] = []
        for exceptions_list in self.exceptions_summary.values():
            for exception in exceptions_list:
                exceptions.append(exception)
        return ContentValidationSummary.build_from_exceptions(exceptions)
