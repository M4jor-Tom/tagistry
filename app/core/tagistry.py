from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from core.config import PROFILE, ROLE, APP_NAME
from rest import health_router
from rest.api import api_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 {} is starting with profile [{}] and role [{}]", APP_NAME.capitalize(), PROFILE.value, ROLE.value)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(api_router)
