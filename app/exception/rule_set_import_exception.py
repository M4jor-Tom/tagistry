from exception import DomainException


class RuleSetImportException(DomainException):
    pass

class RuleSetElementPathDoesNotExist(RuleSetImportException):
    reason = "rule set element path does not exist"
    path: str

    def __init__(self, path: str):
        super().__init__(path)
