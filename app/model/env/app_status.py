from enum import Enum

from pydantic import BaseModel


class AppStatusEnum(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class AppStatus(BaseModel):
    status: AppStatusEnum
