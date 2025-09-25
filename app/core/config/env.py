import os
import logging

from core.model.env import Role, Profile

logger = logging.getLogger(__name__)

class Env:
    @staticmethod
    def get(key: str, default: str | None = None) -> str:
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Missing env var: {key}")
        return value

    def get_role(self, default: Role) -> Role:
        return Role.role_from_value(self.get_enum("ROLE", default.value, Role.get_available_roles()))

    def get_profile(self, default: Profile) -> Profile:
        return Profile.profile_from_value(
            self.get_enum("PROFILE", default.value, Profile.get_available_profiles()))

    @staticmethod
    def get_enum(key: str, default: str, options: list[str]) -> str:
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Missing env var: {key}")
        elif value not in options:
            raise ValueError(f"Env var: {key} has invalid value: {value}. Should be within {str(options)}")
        return value

    @staticmethod
    def get_int(key: str, default: int | None = None) -> int:
        val = os.getenv(key)
        if val is None:
            if default is not None:
                return default
            raise ValueError(f"Missing env var: {key}")
        return int(val)

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        val = os.getenv(key)
        return val.lower() in {"1", "true", "yes", "on"} if val else default
