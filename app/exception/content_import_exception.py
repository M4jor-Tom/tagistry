from exception import DomainException

class ContentImportException(DomainException):
    path: str

class FileNameWithoutSpaces(ContentImportException):
    reason = "tags part must have a space with the content title "
    "('<tags> <file_name>' instead of '<tags><file_name>')"

    def __init__(self, path: str):
        super().__init__(path)


class UntaggedContentFile(ContentImportException):
    reason = "content file is untagged"

    def __init__(self, path: str):
        super().__init__(path)
