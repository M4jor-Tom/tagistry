from exception import DomainException


class ContentImportException(DomainException):
    pass


class FileNameWithoutSpacesException(ContentImportException):
    key = "file_names_without_spaces"
    reason = "tags part must have a space with the content title ('<tags> <file_name>' instead of '<tags><file_name>')"


class TagNotAllowedException(ContentImportException):
    key = "tags_not_allowed"
    reason = "the following tag is unallowed"


class UntaggedContentFileException(ContentImportException):
    key = "untagged_content_file_names"
    reason = "content file is untagged"

class MissingParentTagValueException(ContentImportException):
    key = "missing_parent_tag"
    reason = None
