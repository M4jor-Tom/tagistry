class DomainException(Exception):
    reason: str

    def get_details(self) -> str:
        return self.reason
