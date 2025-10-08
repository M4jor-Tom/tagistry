from fastapi import APIRouter

from constant import example_strip, master

example_router: APIRouter = APIRouter()

@example_router.get(path=example_strip, tags=[master])
def example_get() -> dict[str, str]:
    return {"example": "data"}
