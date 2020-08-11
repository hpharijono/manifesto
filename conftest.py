import os
import pytest
from django import setup
from django.core.management import call_command


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    setup()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'users.json')
        call_command('loaddata', 'values.json')
        call_command('loaddata', 'principles.json')