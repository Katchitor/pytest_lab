import pytest
from calculator import Calculator
from app import app as flask_app


@pytest.fixture
def calc():
    return Calculator()


@pytest.fixture
def app():
    # Переводим Flask в режим тестирования
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "local-pytest-secret-key",
    })
    return flask_app


@pytest.fixture
def client(app):
    # Возвращает клиент, который умеет делать GET/POST запросы и сохранять сессию
    return app.test_client()
