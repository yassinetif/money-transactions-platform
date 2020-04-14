from entity.models import Entity
from entity.models import Agent
from shared.models import Account


class EntityRepository():

    @staticmethod
    def fetch_by_agent(agent: Agent) -> dict:
        try:
            entity = Entity.objects.get(agent=agent)
            entity_dict = entity.to_dict()
            entity_dict.update({'country': entity.country.iso})
            return entity_dict
        except Agent.DoesNotExist:
            return {}

    @staticmethod
    def fetch_all_ancestors(entity: Entity) -> list:
        result = [e for e in entity.get_ancestors(include_self=True)]
        return result
