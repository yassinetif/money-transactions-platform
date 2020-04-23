import pytest
from entity.models import Entity, Agent
from tests.fixtures.shared_fixture import country
from django.contrib.auth.models import User


@pytest.fixture
def entity(country):
    entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@test.com',
        'address': 'Dakar'
    })
    entity.country = country
    entity.save()
    return entity


@pytest.fixture
def entity_payload(country):
    return Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@test.com',
        'address': 'Dakar'
    })


@pytest.fixture
def agent(entity):

    user = User(**{
        'username': 'test',
        'password': 'password',
        'email': 'test@test.com',
    })
    user.save()

    agent = Agent(**{
        'phone_number': '777777',
        'address': 'TEST',
    })
    agent.informations = user
    agent.entity = entity
    agent.save()
    return agent
