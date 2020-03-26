from entity.models import Agent

class AgentRepository():

    @staticmethod
    def fetch_by_user(self, user):
        try:
            return Agent.objects.get(user = user)
        except Agent.DoesNotExist:
            return None