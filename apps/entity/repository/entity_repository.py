from entity.models.entity import Entity
from entity.models.agent import Agent
from core.errors import AgentException

class EntityRepository():

    @staticmethod
    def fetch_by_agent(agent):
        try:
            entity = Entity.objects.get(agent=agent)
            entity_dict = entity.to_dict()
            entity_dict.update({'country': entity.country.iso})
            return entity_dict
        except Agent.DoesNotExist:
            raise AgentException('agent does not exist', {'response_code': 'ERR', 'response_text': 'unknown agent'})

    @staticmethod
    def fetch_all_ancestors(entity):
        result = [e for e in entity.get_ancestors(include_self=True)]
        return result
