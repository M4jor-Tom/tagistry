from fastapi import APIRouter, Depends

from constant import master, send_rule_set_dir_strip
from core.config import CONTENT_FILE_PATH_BLACKLIST_STRIP
from model.domain import Tag
from service import RuleSetService, get_rule_set_service

rule_set_dir_router: APIRouter = APIRouter()


@rule_set_dir_router.post(path=send_rule_set_dir_strip, tags=[master])
def send_rule_set_dir(rule_set_dir: str,
                      banned_strips: tuple[str, ...] = CONTENT_FILE_PATH_BLACKLIST_STRIP,
                      rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> list[Tag]:
    rule_set_service.import_rule_set(rule_set_dir, banned_strips)
    return rule_set_service.tags
