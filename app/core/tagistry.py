import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import PROFILE, ROLE

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Tagistry is starting with profile [{PROFILE.value}] and role [{ROLE.value}]...")
    yield

app = FastAPI(lifespan=lifespan)
