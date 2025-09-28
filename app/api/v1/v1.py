from fastapi import APIRouter

from constant import v1_strip
from .content_file_dir import content_file_dir_router
from .rule_set_dir import rule_set_dir_router

v1_router: APIRouter = APIRouter(prefix=v1_strip)

v1_router.include_router(content_file_dir_router)
v1_router.include_router(rule_set_dir_router)
