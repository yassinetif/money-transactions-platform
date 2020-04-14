from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from entity.models import Agent, Entity
from shared.models import Account, Country
from django.contrib.contenttypes.models import ContentType


def get_country_obj():
    country = Country(**{
        'iso': 'SN'
    })
    return country


def get_entity_obj():
    entity = Entity(**{
        'category': 'PROVIDER',
        'phone_number': 'XXXXXXX',
        'email': 'test@test.com',
        'address': 'Dakar'
    })
    return entity


def create_entity(entity, country):
    country.save()
    entity.country = country
    entity.save()
    return entity


class UserTest(TestCase):

    def setUp(self):
        super(UserTest, self).setUp()
        self.country = get_country_obj()
        self.entity = get_entity_obj()

    def test_entity_is_not_created(self):
        count = Entity.objects.all().count()
        self.assertEqual(count, 0)

    def test_entity_is_created(self):
        create_entity(self.entity, self.country)
        count = Entity.objects.all().count()
        self.assertEqual(count, 1)

    def test_account_is_created(self):
        create_entity(self.entity, self.country)
        entity_content_type = ContentType.objects.get_for_model(Entity)

        result = Account.objects.filter(
            content_type=entity_content_type, object_id=self.entity.id).count()
        self.assertEqual(result, 1)
