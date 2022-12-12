import pytest
import jwt
import json
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_login_endpoint(client):
    # Request with correct credentials
    response = client.post("/api/queue/login", json={
        "user":"testUser1",
        "password":"1234"
    })
    
    assert response.status_code == 200
    assert 'token' in response.json
    
    if response.status_code == 200:
        token = response.json['token']
        decoded = jwt.decode(token,"MySecretKey", algorithms=['HS256'])
        assert decoded['user'] == 'testUser1'

    #Request with invalid credentials
    response = client.post("/api/queue/login", json={
        "user":"1",
        "password":"12"
    })

    assert response.status_code == 401