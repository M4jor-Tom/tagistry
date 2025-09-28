from __future__ import annotations

from enum import Enum

class Role(Enum):
    default = "default"

    @staticmethod
    def role_from_value(value: str) -> Role:
        for profile in Role:
            if profile.value == value:
                return profile
        raise ValueError(f"Unknown profile value: {value}")

    @staticmethod
    def get_available_roles() -> list[str]:
        return [e.name for e in Role]
