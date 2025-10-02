import hashlib
import os
import re
from pathlib import Path

from loguru import logger

from exception import ContentImportException, FileNameWithoutSpacesException, UntaggedContentFileException, \
    TagNotAllowedException, MissingParentTagValueException
from model.domain import ContentFile, Tag
from service import RuleSetService


class ContentFileService:

    def __init__(self, rule_set_service: RuleSetService):
        self.content_files: list[ContentFile] = []
        self.parsed_tag_values: set[str] = set()
        self.exceptions_summary: dict[type[ContentImportException], list[ContentImportException]] = {}
        self.content_validation_summary: dict[str, list[str]] = {}
        self.rule_set_service: RuleSetService = rule_set_service

    def _handle_content_import_exception(self, exception: ContentImportException):
        exception_type: type[ContentImportException] = type(exception)
        if exception_type not in self.exceptions_summary:
            self.exceptions_summary[exception_type] = []
        self.exceptions_summary[exception_type].append(exception)
        if exception.key not in self.content_validation_summary:
            self.content_validation_summary[exception.key] = []
        self.content_validation_summary[exception.key].append(exception.value)

    def sanitize_tags(self, path: str, file_name: str) -> list[str]:
        file_name_split: list[str] = file_name.split(" ")
        if len(file_name_split) < 1:
            raise FileNameWithoutSpacesException(path)
        tags_part: str = file_name_split[0]
        tags: list[str] = re.findall(r"{(\w+)}+", tags_part)
        if len(tags) == 0:
            raise UntaggedContentFileException(path)
        for tag in tags:
            self.parsed_tag_values.add(tag)
        return tags

    def check_disallowed_tags_amongst_content_files(self) -> tuple[list[str], list[TagNotAllowedException]]:
        allowed_tag_values: list[str] = []
        tag_value_not_allowed_exceptions: list[TagNotAllowedException] = []
        for found_tag in self.parsed_tag_values:
            if found_tag in self.rule_set_service.get_tags_values():
                allowed_tag_values.append(found_tag)
            else:
                tag_value_not_allowed_exceptions.append(TagNotAllowedException(found_tag))
        return allowed_tag_values, tag_value_not_allowed_exceptions

    def update_content_files_with_missing_parent_tags(self, content_files: list[ContentFile]):
        for content_file in content_files:
            for content_file_tag_value in content_file.tag_values:
                if content_file_tag_value in self.rule_set_service.tags:
                    content_file_tag: Tag = self.rule_set_service.tags[content_file_tag_value]
                    for parent_tag in content_file_tag.parent_tags:
                        if parent_tag.value not in content_file.tag_values:
                            content_file.missing_tag_values.append(parent_tag.value)
        return content_files

    def build_content_file(self, path: str, content_hash: str | None) -> ContentFile:
        dir_name: str = os.path.dirname(path)
        base_name: str = os.path.basename(path)
        base_name_without_extension, extension = os.path.splitext(base_name)
        tag_values: list[str] = self.sanitize_tags(path, base_name)
        result: ContentFile = ContentFile(
            dir_name=dir_name, base_name_without_extension=base_name_without_extension, extension=extension,
            content_hash=content_hash, tag_values=tag_values, missing_tag_values=[])
        return result

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

    def _log_exceptions_summary(self):
        for exception_type in self.exceptions_summary:
            occurrences_list: list[ContentImportException] = self.exceptions_summary[exception_type]
            logger.error("Refused {} paths for {}", len(occurrences_list), exception_type.reason)
            for exception in occurrences_list:
                logger.warning(exception.get_details())

    def _input_content_file(
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
                            ) -> dict[str, list[str]]:
        for path in Path(content_file_absolute_parent_dir).rglob("*"):
            try:
                if ContentFileService.is_path_to_take(path, banned_strips):
                    relative_file_split: list[str] = str(path).split(content_file_absolute_parent_dir)
                    if len(relative_file_split) == 2:
                        relative_path: str = relative_file_split[1]
                        self._input_content_file(relative_path.lstrip('/'), path, compute_hash)
            except ContentImportException as e:
                self._handle_content_import_exception(e)

        allowed_tag_values, tag_value_not_allowed_exceptions = self.check_disallowed_tags_amongst_content_files()

        for tag_not_allowed_exception in tag_value_not_allowed_exceptions:
            self._handle_content_import_exception(tag_not_allowed_exception)

        for content_file in self.update_content_files_with_missing_parent_tags(self.content_files):
            if len(content_file.missing_tag_values) > 0:
                self._handle_content_import_exception(MissingParentTagValueException(
                    f"content file {content_file.path} misses the following tags: "
                    f"{content_file.missing_tag_values}"))

        self._log_exceptions_summary()
        return self.content_validation_summary
