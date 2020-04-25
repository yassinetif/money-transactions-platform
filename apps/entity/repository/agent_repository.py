from entity.models import Agent
from core.errors import AgentException

class AgentRepository():

    @staticmethod
    def fetch_by_user(user) -> Agent:
        try:
            return Agent.objects.get(informations=user)
        except Agent.DoesNotExist:
            raise AgentException('unknown agent account',err)

    @staticmethod
    def fetch_by_code(code):
        try:
            return Agent.objects.get(code=code)
        except Agent.DoesNotExist as err:
            raise AgentException('unknown agent account',err)

