from fastapi import APIRouter
from fastapi.params import Depends

from core.config import CONTENT_FILE_PATH_BLACKLIST_STRIP
from constant import master, send_content_file_parent_dir_strip
from service import ContentFileService

content_file_dir_router = APIRouter()


@content_file_dir_router.post(send_content_file_parent_dir_strip, tags=[master])
def send_content_file_parent_dir(
        content_file_absolute_parent_dir: str,
        banned_strips: tuple[str, ...] = CONTENT_FILE_PATH_BLACKLIST_STRIP,
        compute_hash: bool = True,
        content_file_service: ContentFileService = Depends(ContentFileService)) -> None:
    content_file_service.input_content_files(
        content_file_absolute_parent_dir,
        banned_strips,
        compute_hash
    )
