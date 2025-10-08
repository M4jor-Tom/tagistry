from fastapi import APIRouter

from rest.api.v1 import v1_router
from constant import api_strip

api_router: APIRouter = APIRouter(prefix=api_strip)

api_router.include_router(v1_router)
