import pytest
from app import create_app
from pytest_mock import mocker

@pytest.fixture()
def test_client():
    flask_app = create_app()
    context = flask_app.app_context()
    context.push()
    return flask_app