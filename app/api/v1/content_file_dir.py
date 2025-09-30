from fastapi import APIRouter
from fastapi.params import Depends

from core.config import DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP, DEFAULT_CONTENT_FILE_DIR
from constant import master, send_content_file_parent_dir_strip
from model.domain import ContentValidationSummary
from service import ContentFileService, get_content_file_service

content_file_dir_router = APIRouter()


@content_file_dir_router.post(send_content_file_parent_dir_strip, tags=[master])
def send_content_file_parent_dir(
        content_file_absolute_parent_dir: str = DEFAULT_CONTENT_FILE_DIR,
        banned_strips: tuple[str, ...] = DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP,
        compute_hash: bool = False,
        content_file_service: ContentFileService = Depends(get_content_file_service)) -> ContentValidationSummary:
    return content_file_service.input_content_files(
        content_file_absolute_parent_dir,
        banned_strips,
        compute_hash
    )
