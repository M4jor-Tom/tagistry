class DomainException(Exception):
    reason: str
    key: str
    value: str
    details: str

    def __init__(self, value: str):
        self.value = value
        self.details = f"{self.reason}: {self.value}"
