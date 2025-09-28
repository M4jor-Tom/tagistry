from __future__ import annotations

from enum import Enum

class Profile(Enum):
    DEV = "DEV"
    PROD = "PROD"

    @staticmethod
    def profile_from_value(value: str) -> Profile:
        for profile in Profile:
            if profile.value == value:
                return profile
        raise ValueError(f"Unknown profile value: {value}")

    @staticmethod
    def get_available_profiles() -> list[str]:
        return [e.name for e in Profile]
