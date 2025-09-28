from exception import DomainException


class RuleSetImportException(DomainException):
    pass

class RuleSetElementPathDoesNotExist(RuleSetImportException):
    reason = "rule set element path does not exist"
    path: str

    def __init__(self, path: str):
        super().__init__(path)

class InconsistentRuleSetException(RuleSetImportException):
    reason = "rule set inconsistent"
    inconsistent_tag_with_mandatory_category: list[tuple[str, list[str]]]

    def __init__(self, inconsistent_tag_with_mandatory_category: list[tuple[str, list[str]]]):
        self.inconsistent_tag_with_mandatory_category = inconsistent_tag_with_mandatory_category

    @staticmethod
    def get_inconsistent_tag_name_detail(inconsistent_tag_with_mandatory_category: tuple[str, list[str]]) -> str:
        inconsistent_tag_value: str = inconsistent_tag_with_mandatory_category[0]
        mandatory_categories: list[str] = inconsistent_tag_with_mandatory_category[1]
        return f"{inconsistent_tag_value} should have the following: {mandatory_categories} categories"

    def get_details(self) -> str:
        details: list[str] = [
            InconsistentRuleSetException.get_inconsistent_tag_name_detail(inconsistency)
            for inconsistency
            in self.inconsistent_tag_with_mandatory_category
        ]
        return f"{self.reason}: {details}"
