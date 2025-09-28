class TagsSanitizingException(Exception):
    reason: str

    def __init__(self, reason: str):
        self.reason = reason


class TagsFileNamePartNotFound(TagsSanitizingException):
    def __init__(self):
        super().__init__("tags part in file name not found")
