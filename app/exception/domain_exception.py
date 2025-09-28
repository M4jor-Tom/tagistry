class DomainException(Exception):
    reason: str

    def __init__(self, path: str):
        self.path = path
