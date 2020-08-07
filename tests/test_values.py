import requests
import pytest
from rest_framework import status
from apps.manifesto.models import Value
from rest_framework.authtoken.models import Token


BASE_URL = 'http://127.0.0.1:8000/api'
VALUES_URL = '{}/{}/'.format(BASE_URL, 'values')
REQUIRED_ERROR = 'This field may not be blank.'

def test_get_values_unauthorized():
    response = requests.get(VALUES_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_values_list():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}
    
    response = requests.get(VALUES_URL, headers=header)

    assert response.status_code == status.HTTP_200_OK

def test_get_values_detail():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}
    
    val = Value.objects.first()
    
    url = '{}{}'.format(VALUES_URL, val.pk)
    response = requests.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['value'] == val.value
    assert response.json()['description'] == val.description

def test_create_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    data = {
        "value": "Test value",
        "description": "Test description",
    }
    values_count = Value.objects.count()

    response = requests.post(VALUES_URL, headers=header, data=data)

    new_values_count = Value.objects.count()

    assert response.status_code == status.HTTP_201_CREATED
    assert values_count + 1 == new_values_count
    assert response.json()['value'] == data['value']
    assert response.json()['description'] == data['description']

def test_create_value_missing_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    data = {
        "value": "",
        "description": "Test description",
    }

    response = requests.post(VALUES_URL, headers=header, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    value = Value.objects.last()
    data = {
        "value": value.value,
        "description": "Updated description",
    }

    url = '{}{}/'.format(VALUES_URL, value.pk)
    response = requests.put(url, data=data, headers=header)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == value.pk
    assert response.json()['value'] == data['value']
    assert response.json()['description'] == data['description']

def test_delete_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    value = Value.objects.last()
    values_count = Value.objects.count()

    url = '{}{}'.format(VALUES_URL, value.pk)

    response = requests.delete(url, headers=header)

    new_values_count = Value.objects.count()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_values_count == values_count - 1 
