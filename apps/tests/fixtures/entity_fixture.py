import pytest
from entity.models import Entity, Agent
from django.contrib.auth.models import User
from shared.models import Country


@pytest.fixture
def entity():
    country = Country(**{
        'iso': 'SN'
    })
    entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@example.com',
        'address': 'Dakar'
    })
    country.save()
    entity.country = country
    entity.save()
    return entity


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
    agent.save()
    return agent
