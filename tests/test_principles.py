from django.contrib.auth.models import User

from pytest_django.asserts import assertContains
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from apps.manifesto.models import Principle

BASE_URL = 'http://127.0.0.1:8000/api'
PRINCIPLES_URL = '{}/{}/'.format(BASE_URL, 'principles')


class TestPriciples(APITestCase):
    def setUp(self):
        user = User.objects.get(username='user1')

        if not user:
            user = User(
                username='harris',
                email='harris@gmail.com',
                first_name='Harris',
                last_name='Harijono'
            )
            user.set_password('harris')
            user.save()

        token, created = Token.objects.get_or_create(user=user)

        if token:
            self.token = token.key

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_principles_unauthorized(self):
        # create client without credentials
        client = APIClient()
        response = client.get(PRINCIPLES_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_principles_list(self):
        response = self.client.get(PRINCIPLES_URL)

        assert response.status_code == status.HTTP_200_OK

    def test_get_principles_detail(self):
        principle = Principle.objects.first()
        
        url = '{}{}/'.format(PRINCIPLES_URL, principle.pk)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['principle'] == principle.principle
        assert response.json()['description'] == principle.description

    def test_create_principle(self):
        data = {
            "principle": "Test principle",
            "description": "Test description",
        }
        principles_count = Principle.objects.count()

        response = self.client.post(PRINCIPLES_URL, data, format='json')

        new_principles_count = Principle.objects.count()

        assert response.status_code == status.HTTP_201_CREATED
        assert principles_count + 1 == new_principles_count
        assert response.json()['principle'] == data['principle']
        assert response.json()['description'] == data['description']

    def test_create_principle_missing_value(self):
        data = {
            "principle": "",
            "description": "Test description",
        }

        response = self.client.post(PRINCIPLES_URL, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_value(self):
        principle = Principle.objects.last()
        data = {
            "principle": principle.principle,
            "description": "Updated principle description",
        }

        url = '{}{}/'.format(PRINCIPLES_URL, principle.pk)
        response = self.client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == principle.pk
        assert response.json()['principle'] == principle.principle
        assert response.json()['description'] == data['description']

    def test_delete_principle(self):
        principle = Principle.objects.last()
        principles_count = Principle.objects.count()

        url = '{}{}/'.format(PRINCIPLES_URL, principle.pk)

        response = self.client.delete(url)

        new_principles_count = Principle.objects.count()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert new_principles_count == principles_count - 1 
