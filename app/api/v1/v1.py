from fastapi import APIRouter

from constant import v1_strip
from .content_file_path import content_file_path_router

v1_router: APIRouter = APIRouter(prefix=v1_strip)

v1_router.include_router(content_file_path_router)
