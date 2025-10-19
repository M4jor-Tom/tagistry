import json

from fastapi import APIRouter, Depends, UploadFile, File

from constant import master, send_rule_set_dir_strip, send_rule_set_file_strip, get_rule_set_tags_view_format_strip, \
    get_rule_set_tags_persistent_format_strip
from core.config import DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP, DEFAULT_RULE_SET_DIR
from model.domain import Tag
from model.persistence import TagJsonObject
from service import RuleSetService, get_rule_set_service

rule_set_router: APIRouter = APIRouter()


@rule_set_router.get(path=get_rule_set_tags_view_format_strip, tags=[master])
def get_rule_set_tags_view_format(rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> dict[str, Tag]:
    return rule_set_service.tags


@rule_set_router.get(path=get_rule_set_tags_persistent_format_strip, tags=[master])
def get_rule_set_tags_persistent_format(rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> list[
    TagJsonObject]:
    return [tag.to_file_json() for name, tag in rule_set_service.tags.items()]


@rule_set_router.post(path=send_rule_set_file_strip, tags=[master])
async def send_rule_set_file(rule_set_file: UploadFile = File(...),
                             rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> dict[str, Tag]:
    return rule_set_service.import_rule_set_by_tags(json.loads(await rule_set_file.read()))


@rule_set_router.post(path=send_rule_set_dir_strip, tags=[master])
def send_rule_set_dir(rule_set_dir: str = DEFAULT_RULE_SET_DIR,
                      banned_strips: tuple[str, ...] = DEFAULT_CONTENT_FILE_PATH_BLACKLIST_STRIP,
                      rule_set_service: RuleSetService = Depends(get_rule_set_service)) -> list[TagJsonObject]:
    rule_set_service.import_rule_set(rule_set_dir, banned_strips)
    return [tag.to_file_json() for name, tag in rule_set_service.tags.items()]
