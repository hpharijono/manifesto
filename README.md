# Agile Software Manifesto

This repository contains a REST API created using Django and Django REST that exposes the 4 values and the 12 principles of Agile Software Development. This API allows the CRUD process of values and principles endpoint. The database used is SQLite

## Requirements

- Python > 3.8
- Pipenv == 2020.6.2

## Usage

Clone the repository

```python
git clone https://github.com/hpharijono/manifesto.git

pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser --username admin
python manage.py loaddata values principles
python manage.py runserver
```

You may now navigate to [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) to use the API

## Testing

Testing is done using pytest.

```python
pytest
```
