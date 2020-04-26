import pytest
from tests.fixtures.entity_fixture import agent, entity, entity_child
from tests.fixtures.shared_fixture import country
from entity.repository.entity_repository import EntityRepository
from core.errors import AgentException
from django.contrib.auth.models import User
from entity.models.agent  import Agent


@pytest.mark.django_db
class TestEntityRepository:

    def test_fetch_by_agent_success(self, agent):
        expected = agent.entity.to_dict()
        expected.update({'country': agent.entity.country.iso})
        result = EntityRepository.fetch_by_agent(agent)
        assert result == expected

    def test_fetch_by_agent_fail(self, agent, entity_child):
        expected = agent.entity.to_dict()
        expected.update({'country': agent.entity.country.iso})

        user = User(**{
            'username': 'TEST',
            'password': 'password',
            'email': 'test2@example1.com',
        })
        user.save()
        _agent: Agent = Agent(**{
            'phone_number': '88888',
            'address': 'TEST',
        })
        _agent.informations = user
        _agent.code = 'TEST'
        _agent.entity = entity_child
        _agent.save()

        result = EntityRepository.fetch_by_agent(_agent)
        assert result != expected

    def test_fetch_all_ancestors(self, entity, entity_child):

        result = EntityRepository.fetch_all_ancestors(entity_child)
        assert entity in result
