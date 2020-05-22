from apps.entity.models.entity import Entity
from apps.core.errors import EntityException, CoreException

ERR = 'Entity does not exist'
ERR_TEXT = 'unable to find entity for this agent'
class EntityRepository():

    @staticmethod
    def fetch_by_agent(agent):
        try:
            entity = agent.entity
            entity_dict = entity.to_dict()
            entity_dict.update({'country': entity.country.iso})
            return entity_dict
        except Entity.DoesNotExist:
            raise EntityException(ERR, {'response_code': '100', 'response_text': ERR})

    @staticmethod
    def fetch_by_agent_code(code):
        try:
            return Entity.objects.get(agent__code=code)
        except Entity.DoesNotExist:
            raise EntityException(ERR, {'response_code': '100', 'response_text': ERR})

    @staticmethod
    def fetch_by_account_number(account_number):
        try:
            return Entity.objects.get(account_number=account_number)
        except Entity.DoesNotExist:
            raise EntityException(ERR, {'response_code': '100', 'response_text': ERR})

    @staticmethod
    def fetch_all_ancestors(entity):
        result = [e for e in entity.get_ancestors(include_self=True)]
        return result

    @staticmethod
    def fetch_entity_by_type_and_hierarchy(_entity, entity_type):
        try:
            entity_ancestors = [_e.brand_name for _e in EntityRepository.fetch_all_ancestors(_entity)]
            entity = Entity.objects.get(category=entity_type, brand_name__in=entity_ancestors)
            return entity
        except Exception as err:
            raise CoreException(err, 'unable to fetch right entity')
