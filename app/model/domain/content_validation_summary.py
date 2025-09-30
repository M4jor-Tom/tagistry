from __future__ import annotations

from pydantic import BaseModel

from exception import ContentImportException, FileNameWithoutSpacesException, UntaggedContentFileException, \
    TagNotAllowedException


class ContentValidationSummary(BaseModel):
    files_name_without_spaces: list[str]
    untagged_content_file_names: list[str]
    tags_not_allowed: list[str]

    @staticmethod
    def build_from_exceptions(
            content_import_exceptions: list[ContentImportException]) -> ContentValidationSummary:
        content_validation_summary: ContentValidationSummary = ContentValidationSummary(
            files_name_without_spaces=[],
            untagged_content_file_names=[],
            tags_not_allowed=[]
        )
        for exception in content_import_exceptions:
            if isinstance(exception, FileNameWithoutSpacesException):
                content_validation_summary.files_name_without_spaces.append(exception.path)
            elif isinstance(exception, UntaggedContentFileException):
                content_validation_summary.untagged_content_file_names.append(exception.path)
            elif isinstance(exception, TagNotAllowedException):
                content_validation_summary.tags_not_allowed.append(exception.unknown_tag)
        return content_validation_summary
