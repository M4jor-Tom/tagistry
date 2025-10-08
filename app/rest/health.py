from fastapi import APIRouter

from constant import health_strip, system
from model.env import AppStatus, AppStatusEnum

health_router: APIRouter = APIRouter()

@health_router.get(path=health_strip, tags=[system])
def get_health() -> AppStatus:
    return AppStatus(status=AppStatusEnum.PASS)
