from entity.models.entity import Entity
from core.errors import EntityException

ERR = 'Entity does not exist'
ERR_TEXT = 'unable to find entity for this agent'
class EntityRepository():

    @staticmethod
    def fetch_by_agent(agent):
        try:
            entity = Entity.objects.get(agent=agent)
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
