from fastapi import APIRouter, Depends

from constant import master, send_rule_set_dir_strip
from core.config import DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP, DEFAULT_RULE_SET_DIR
from model.domain import Tag
from model.persistence import TagJsonModel
from service import RuleSetService, get_rule_set_service

rule_set_dir_router: APIRouter = APIRouter()


@rule_set_dir_router.post(path=send_rule_set_dir_strip, tags=[master])
def send_rule_set_dir(rule_set_dir: str = DEFAULT_RULE_SET_DIR,
                      banned_strips: tuple[str, ...] = DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP,
                      rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> list[TagJsonModel]:
    rule_set_service.import_rule_set(rule_set_dir, banned_strips)
    return [tag.to_file_json() for name, tag in rule_set_service.tags.items()]
