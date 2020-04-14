from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from django.test.client import RequestFactory


class UserTest(TestCase):

    def setUp(self):
        super(UserTest, self).setUp()
        self.user = User(**{
            'username': 'test',
            'password': 'password',
            'email': 'test@example.com'
        })
        self.user.set_password('password')
        self.user.save()

    def test_user_is_created(self):
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_can_connect(self):
        result = self.user.check_password('password')
        self.assertEqual(result, True)
