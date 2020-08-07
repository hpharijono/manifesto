import requests
import pytest
from rest_framework import status
from apps.manifesto.models import Principle
from rest_framework.authtoken.models import Token


BASE_URL = 'http://127.0.0.1:8000/api'
PRINCIPLES_URL = '{}/{}/'.format(BASE_URL, 'principles')
REQUIRED_ERROR = 'This field may not be blank.'

def test_get_principles_unauthorized():
    response = requests.get(PRINCIPLES_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_principles_list():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}
    
    response = requests.get(PRINCIPLES_URL, headers=header)

    assert response.status_code == status.HTTP_200_OK

def test_get_principles_detail():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}
    
    principle = Principle.objects.first()
    
    url = '{}{}'.format(PRINCIPLES_URL, principle.pk)
    response = requests.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['principle'] == principle.principle
    assert response.json()['description'] == principle.description

def test_create_principle():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    data = {
        "principle": "Test principle",
        "description": "Test description",
    }
    principles_count = Principle.objects.count()

    response = requests.post(PRINCIPLES_URL, headers=header, data=data)

    new_principles_count = Principle.objects.count()

    assert response.status_code == status.HTTP_201_CREATED
    assert principles_count + 1 == new_principles_count
    assert response.json()['principle'] == data['principle']
    assert response.json()['description'] == data['description']

def test_create_principle_missing_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    data = {
        "principle": "",
        "description": "Test description",
    }

    response = requests.post(PRINCIPLES_URL, headers=header, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_value():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    principle = Principle.objects.last()
    data = {
        "principle": principle.principle,
        "description": "Updated principle description",
    }

    url = '{}{}/'.format(PRINCIPLES_URL, principle.pk)
    response = requests.put(url, data=data, headers=header)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == principle.pk
    assert response.json()['principle'] == principle.principle
    assert response.json()['description'] == data['description']

def test_delete_principle():
    token = Token.objects.first()
    header = {'Authorization' : 'Token {}'.format(token)}

    principle = Principle.objects.last()
    principles_count = Principle.objects.count()

    url = '{}{}'.format(PRINCIPLES_URL, principle.pk)

    response = requests.delete(url, headers=header)

    new_principles_count = Principle.objects.count()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_principles_count == principles_count - 1 
