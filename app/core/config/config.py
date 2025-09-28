from .env import Env
from model.env import Role, Profile

env = Env()

APP_NAME: str = "tagistry"
ROLE: Role = env.get_role(Role.default)
PROFILE: Profile = env.get_profile(Profile.PROD)
APP_HOST: str = env.get("APP_HOST", "127.0.0.1")
APP_PORT: int = env.get_int("APP_PORT", 8000)
LOGGING_LEVEL: str = env.get("LOGGING_LEVEL", "INFO")
CONTENT_FILE_PATH_BLACKLIST_STRIP: tuple[str, ...] = env.get_list("CONTENT_FILE_PATH_BLACKLIST_STRIP", "@eaDir:.tar.gz:.sh:.git")
