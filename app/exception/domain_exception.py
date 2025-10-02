class DomainException(Exception):
    reason: str
    key: str
    value: str

    def __init__(self, value: str):
        self.value = value

    def get_details(self) -> str:
        return f"{self.reason}: {self.value}"
