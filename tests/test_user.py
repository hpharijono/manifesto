from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from pytest_django.asserts import assertContains
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

BASE_URL = 'http://127.0.0.1:8000/api'
AUTH_URL = '{}/{}/'.format(BASE_URL, 'token')


class TestUser(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        # Fix the passwords of fixtures
        for user in self.User.objects.all():
            user.set_password(user.password)
            user.save()

        self.client = APIClient()

    def test_auth_token(self):
        # user = User(
        #     username='harris',
        #     email='harris@gmail.com',
        #     first_name='Harris',
        #     last_name='Harijono'
        # )
        # user.set_password('harris')
        # user.save()

        body = {
            "username": "user1",
            "password": "user1"
        }

        response = self.client.post(AUTH_URL, body, format='json')

        assertContains(response, 'token', status_code=status.HTTP_200_OK)


