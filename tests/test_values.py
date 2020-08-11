from django.contrib.auth.models import User

from pytest_django.asserts import assertContains
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from apps.manifesto.models import Value

BASE_URL = 'http://127.0.0.1:8000/api'
VALUES_URL = '{}/{}/'.format(BASE_URL, 'values')
REQUIRED_ERROR = 'This field may not be blank.'


class TestValues(APITestCase):
    def setUp(self):
        user = User.objects.get(username='user1')

        if not user:
            user = User(
                username='harris1',
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

    def test_get_values_unauthorized(self):
        # create client without credentials
        client = APIClient()
        response = client.get(VALUES_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_values_list(self):
        response = self.client.get(VALUES_URL)

        assert response.status_code == status.HTTP_200_OK

    def test_get_values_detail(self):
        val = Value.objects.first()

        url = '{}{}/'.format(VALUES_URL, val.pk)
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['value'] == val.value
        assert response.json()['description'] == val.description

    def test_create_value(self):
        data = {
            "value": "Test value",
            "description": "Test description",
        }
        values_count = Value.objects.count()

        response = self.client.post(VALUES_URL, data, format='json')

        new_values_count = Value.objects.count()

        assert response.status_code == status.HTTP_201_CREATED
        assert values_count + 1 == new_values_count
        assert response.json()['value'] == data['value']
        assert response.json()['description'] == data['description']

    def test_create_value_missing_value(self):
        data = {
            "value": "",
            "description": "Test description",
        }

        response = self.client.post(VALUES_URL, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_value(self):
        value = Value.objects.last()
        data = {
            "value": value.value,
            "description": "Updated description",
        }

        url = '{}{}/'.format(VALUES_URL, value.pk)
        response = self.client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == value.pk
        assert response.json()['value'] == data['value']
        assert response.json()['description'] == data['description']

    def test_delete_value(self):
        value = Value.objects.last()
        values_count = Value.objects.count()

        url = '{}{}/'.format(VALUES_URL, value.pk)

        response = self.client.delete(url)

        new_values_count = Value.objects.count()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert new_values_count == values_count - 1 







