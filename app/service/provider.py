from service import ContentFileService, RuleSetService

rule_set_service: RuleSetService = RuleSetService()
content_file_service: ContentFileService = ContentFileService(rule_set_service)

def get_rule_set_service() -> RuleSetService:
    return rule_set_service

def get_content_file_service() -> ContentFileService:
    return content_file_service
