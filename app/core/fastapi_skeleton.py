from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from api.v1 import v1_router
from core.config import PROFILE, ROLE
from core.config.config import APP_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 {} is starting with profile [{}] and role [{}]", APP_NAME.capitalize(), PROFILE.value, ROLE.value)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
