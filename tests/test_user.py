import pytest

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from pytest_django.asserts import assertContains
from rest_framework import status
from rest_framework.test import APIClient

from conftest import client

AUTH_URL = "/{}/{}/".format("api", "token")


@pytest.mark.django_db
def test_auth_token(client):
    # user = User(
    #     username='harris',
    #     email='harris@gmail.com',
    #     first_name='Harris',
    #     last_name='Harijono'
    # )
    # user.set_password('harris')
    # user.save()

    body = {"username": "admin", "password": "admin"}

    response = client.post(AUTH_URL, body, format="json")

    assertContains(response, "token", status_code=status.HTTP_200_OK)
