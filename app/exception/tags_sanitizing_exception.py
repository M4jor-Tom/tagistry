class TagsSanitizingException(Exception):
    reason: str
    path: str

    def __init__(self, path: str):
        self.path = path


class FileNameWithoutSpaces(TagsSanitizingException):
    reason = "tags part must have a space with the content title "
    "('<tags> <file_name>' instead of '<tags><file_name>')"

    def __init__(self, path: str):
        super().__init__(path)


class UntaggedContentFile(TagsSanitizingException):
    reason = "content file is untagged"

    def __init__(self, path: str):
        super().__init__(path)
