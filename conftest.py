import os
import pytest
from django import setup
from django.core.management import call_command


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json")
        call_command("loaddata", "values.json")
        call_command("loaddata", "principles.json")


@pytest.fixture(name="client")
def client():
    from rest_framework.test import APIClient
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    user = User.objects.get(username="user1")

    if not user:
        user = User(
            username="harris1",
            email="harris@gmail.com",
            first_name="Harris",
            last_name="Harijono",
        )
        user.set_password("harris")
        user.save()

    token, created = Token.objects.get_or_create(user=user)

    if token:
        auth_token = token.key

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + auth_token)
    return client
