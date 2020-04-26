import pytest
from entity.models .entity import Entity
from entity.models.agent import Agent
from django.contrib.auth.models import User
from shared.models.country import Country


@pytest.fixture
def entity():
    country = Country(**{
        'iso': 'SN'
    })
    entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test2@example.com',
        'address': 'Dakar'
    })
    country.save()
    entity.country = country
    entity.save()
    return entity


@pytest.fixture
def entity_child(entity):
    country = Country(**{
        'iso': 'SN'
    })
    _entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@example.com',
        'address': 'Dakar',
        'code': '12345',
        'account_number': '47Z34543'
    })
    country.save()
    _entity.country = country
    _entity.parent = entity
    _entity.save()
    return _entity


@pytest.fixture
def entity_payload(country):
    entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@example.com',
        'address': 'Dakar'
    })
    return entity


@pytest.fixture
def agent(entity):

    user = User(**{
        'username': 'fidelis',
        'password': 'password',
        'email': 'test@example1.com',
    })
    user.save()

    agent = Agent(**{
        'phone_number': '777777',
        'address': 'TEST',
    })
    agent.informations = user
    agent.entity = entity
    agent.code = 'AGENT_CODE'
    agent.save()
    return agent


@pytest.fixture
def other_agent(entity_child):

    user = User(**{
        'username': 'semper',
        'password': 'password',
        'email': 'test@example1.com',
    })
    user.save()

    other_agent = Agent(**{
        'phone_number': '88888',
        'address': 'TEST',
    })
    other_agent.informations = user
    other_agent.entity = entity_child
    other_agent.code = 'AUTRE_AGENT'
    other_agent.save()
    return other_agent
