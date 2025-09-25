from core.config import Env
from core.model.env import Role, Profile

env = Env()

ROLE = env.get_role(Role.default)
PROFILE = env.get_profile(Profile.PROD)
APP_HOST = env.get("APP_HOST", "127.0.0.1")
APP_PORT = env.get_int("APP_PORT", 8000)
LOGGING_LEVEL = env.get("LOGGING_LEVEL", "INFO")
