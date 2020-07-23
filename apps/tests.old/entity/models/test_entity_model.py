import pytest
from tests.fixtures.entity_fixture import entity_payload, entity, agent
from tests.fixtures.shared_fixture import country


@pytest.mark.django_db
class TestEntityModel:

    def test_entity_is_created(self, entity_payload, country):
        obj_entity = entity_payload
        obj_entity.country = country
        obj_entity.save()
        assert obj_entity.pk == 1

    def test_entity_has_account(self, entity):
        assert entity.accounts.count() == 1

    def test_agent_is_created(self, agent):
        assert agent.pk == 1
        assert agent.entity is not None
