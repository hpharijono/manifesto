import pytest

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from apps.manifesto.models import Principle
from conftest import client

PRINCIPLES_URL = "/{}/{}/".format("api", "principles")


@pytest.mark.django_db
def test_get_principles_unauthorized(client):
    # create client without credentials
    client = APIClient()
    response = client.get(PRINCIPLES_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_principles_list(client):
    response = client.get(PRINCIPLES_URL)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_principles_detail(client):
    principle = Principle.objects.first()

    url = "{}{}/".format(PRINCIPLES_URL, principle.pk)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["principle"] == principle.principle
    assert response.json()["description"] == principle.description


@pytest.mark.django_db
def test_create_principle(client):
    data = {
        "principle": "Test principle",
        "description": "Test description",
    }
    principles_count = Principle.objects.count()

    response = client.post(PRINCIPLES_URL, data, format="json")

    new_principles_count = Principle.objects.count()

    assert response.status_code == status.HTTP_201_CREATED
    assert principles_count + 1 == new_principles_count
    assert response.json()["principle"] == data["principle"]
    assert response.json()["description"] == data["description"]


@pytest.mark.django_db
def test_create_principle_missing_value(client):
    data = {
        "principle": "",
        "description": "Test description",
    }

    response = client.post(PRINCIPLES_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_value(client):
    principle = Principle.objects.last()
    data = {
        "principle": principle.principle,
        "description": "Updated principle description",
    }

    url = "{}{}/".format(PRINCIPLES_URL, principle.pk)
    response = client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == principle.pk
    assert response.json()["principle"] == principle.principle
    assert response.json()["description"] == data["description"]


@pytest.mark.django_db
def test_delete_principle(client):
    principle = Principle.objects.last()
    principles_count = Principle.objects.count()

    url = "{}{}/".format(PRINCIPLES_URL, principle.pk)

    response = client.delete(url)

    new_principles_count = Principle.objects.count()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_principles_count == principles_count - 1
