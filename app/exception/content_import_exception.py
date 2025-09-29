from exception import DomainException


class ContentImportException(DomainException):
    path: str

    def __init__(self, path: str):
        self.path = path


class FileNameWithoutSpaces(ContentImportException):
    reason = "tags part must have a space with the content title "
    "('<tags> <file_name>' instead of '<tags><file_name>')"


class TagNotAllowedException(ContentImportException):
    reason = "tag not allowed found"
    unknown_tag: str

    def __init__(self, unknown_tag: str):
        self.unknown_tag = unknown_tag

    def get_details(self) -> str:
        return f"the following tag is unallowed: {self.unknown_tag}"


class UntaggedContentFile(ContentImportException):
    reason = "content file is untagged"

    def get_details(self) -> str:
        return f"content file is untagged: {self.path}"
