from fastapi import APIRouter

from constant import v1_strip
from .example import example_router

v1_router: APIRouter = APIRouter(prefix=v1_strip)

v1_router.include_router(example_router)
