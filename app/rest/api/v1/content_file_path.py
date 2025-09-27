from pathlib import Path

from fastapi import APIRouter

from core.config import CONTENT_FILE_PATH_BLACKLIST_STRIP
from constant import master, send_content_file_parent_dir_strip

content_file_path_router = APIRouter()

def is_path_to_take(path: Path, banned_strips: tuple[str, ...]) -> bool:
    for blacklisted in banned_strips:
        if blacklisted in str(path):
            return False
    return path.is_file()

@content_file_path_router.post(send_content_file_parent_dir_strip, tags=[master])
def send_content_file_parent_dir(content_file_absolute_parent_dir: str, banned_strips: tuple[str, ...] = CONTENT_FILE_PATH_BLACKLIST_STRIP) -> None:
    for file in Path(content_file_absolute_parent_dir).rglob("*"):
        if is_path_to_take(file, banned_strips):
            relative_file_split: list[str] = str(file).split(content_file_absolute_parent_dir)
            if len(relative_file_split) == 2:
                relative_path: str = relative_file_split[1]
                print(relative_path)
