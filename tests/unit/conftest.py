import pytest
from app import create_app
from pytest_mock import mocker


@pytest.fixture()
def test_client():
    flask_app = create_app()
    context = flask_app.app_context()
    context.push()
    flask_app.config.update({
        "TESTING": True,
    })
    return flask_app

@pytest.fixture()
def client(test_client):
    return test_client.test_client()


@pytest.fixture()
def runner(app):
   return app.test_cli_runner()

