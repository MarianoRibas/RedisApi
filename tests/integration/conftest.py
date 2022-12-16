import pytest
from app import create_app
import os
from dotenv import load_dotenv

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()