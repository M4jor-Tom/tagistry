class DomainException(Exception):
    reason: str | None
    key: str
    value: str

    def __init__(self, value: str):
        self.value = value

    def get_details(self) -> str:
        if self.reason is None:
            return self.value
        return f"{self.reason}: {self.value}"
