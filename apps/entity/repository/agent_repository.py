from entity.models.agent import Agent
from core.errors import AgentException

class AgentRepository():

    @staticmethod
    def fetch_by_user(user):
        try:
            return Agent.objects.get(informations=user)
        except Agent.DoesNotExist:
            raise AgentException('unknown agent account', {'response_code': 'ERR', 'response_text': 'unknown agent'})

    @staticmethod
    def fetch_by_username(username):
        try:
            return Agent.objects.get(informations__username=username)
        except Agent.DoesNotExist:
            raise AgentException('unknown agent account', {'response_code': 'ERR', 'response_text': 'unknown agent'})

    @staticmethod
    def fetch_by_code(code):
        try:
            return Agent.objects.get(code=code)
        except Agent.DoesNotExist:
            raise AgentException('unknown agent account', {'response_code': 'ERR', 'response_text': 'unknown agent'})
