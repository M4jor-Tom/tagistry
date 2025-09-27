from core.config import Env
from core.model.env import Role, Profile

env = Env()

ROLE: Role = env.get_role(Role.default)
PROFILE: Profile = env.get_profile(Profile.PROD)
APP_HOST: str = env.get("APP_HOST", "127.0.0.1")
APP_PORT: int = env.get_int("APP_PORT", 8000)
LOGGING_LEVEL: str = env.get("LOGGING_LEVEL", "INFO")
