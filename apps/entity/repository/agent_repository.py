from apps.entity.models.agent import Agent
from apps.core.errors import AgentException
from apps.entity.repository.entity_repository import EntityRepository

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

    @staticmethod
    def to_json(code):
        try:
            agent = Agent.objects.get(code=code)
            data = {}
            data.update({'code': agent.code})
            data.update({'username': agent.informations.username})
            data.update({'first_name': agent.informations.first_name})
            data.update({'last_name': agent.informations.last_name})
            data.update({'entity': EntityRepository.to_json(code)})
            return data
        except Agent.DoesNotExist:
            raise AgentException('unknown agent account', {'response_code': 'ERR', 'response_text': 'unknown agent'})

    @staticmethod
    def get_batch_agent():
        return Agent.objects.get(nformations__username='BATCH')
