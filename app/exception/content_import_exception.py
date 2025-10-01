from exception import DomainException


class ContentImportException(DomainException):
    key: str
    value: str
    path: str

    def __init__(self, path: str):
        self.path = path

    def get_details(self) -> str:
        return f"{self.reason}: {self.path}"


class FileNameWithoutSpacesException(ContentImportException):
    key = "file_names_without_spaces"
    reason = "tags part must have a space with the content title ('<tags> <file_name>' instead of '<tags><file_name>')"

    def __init__(self, path: str):
        super().__init__(path)
        self.value = path


class TagNotAllowedException(ContentImportException):
    key = "tags_not_allowed"
    reason = "tag not allowed found"
    unknown_tag: str

    def __init__(self, unknown_tag: str):
        self.unknown_tag = unknown_tag
        self.value = unknown_tag

    def get_details(self) -> str:
        return f"the following tag is unallowed: {self.unknown_tag}"


class UntaggedContentFileException(ContentImportException):
    key = "untagged_content_file_names"
    reason = "content file is untagged"

    def __init__(self, path: str):
        super().__init__(path)
        self.value = path

    def get_details(self) -> str:
        return f"content file is untagged: {self.path}"
