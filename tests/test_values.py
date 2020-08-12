import pytest

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from apps.manifesto.models import Value
from conftest import client

VALUES_URL = "/{}/{}/".format("api", "values")


@pytest.mark.django_db
def test_get_values_unauthorized(client):
    # create client without credentials
    client = APIClient()
    response = client.get(VALUES_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_values_list(client):
    response = client.get(VALUES_URL)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_values_detail(client):
    val = Value.objects.first()

    url = "{}{}/".format(VALUES_URL, val.pk)
    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == val.value
    assert response.json()["description"] == val.description


@pytest.mark.django_db
def test_create_value(client):
    data = {
        "value": "Test value",
        "description": "Test description",
    }
    values_count = Value.objects.count()

    response = client.post(VALUES_URL, data, format="json")

    new_values_count = Value.objects.count()

    assert response.status_code == status.HTTP_201_CREATED
    assert values_count + 1 == new_values_count
    assert response.json()["value"] == data["value"]
    assert response.json()["description"] == data["description"]


@pytest.mark.django_db
def test_create_value_missing_value(client):
    data = {
        "value": "",
        "description": "Test description",
    }

    response = client.post(VALUES_URL, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_value(client):
    value = Value.objects.last()
    data = {
        "value": value.value,
        "description": "Updated description",
    }

    url = "{}{}/".format(VALUES_URL, value.pk)
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == value.pk
    assert response.json()["value"] == data["value"]
    assert response.json()["description"] == data["description"]


@pytest.mark.django_db
def test_delete_value(client):
    value = Value.objects.last()
    values_count = Value.objects.count()

    url = "{}{}/".format(VALUES_URL, value.pk)

    response = client.delete(url)

    new_values_count = Value.objects.count()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_values_count == values_count - 1
