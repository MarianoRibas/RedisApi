from pytest_mock import mocker
from services.services import pop_item
from conftest import client

def test_login_endpoint_success(client, mocker):
    mocker.patch('apis.auth.login', return_value = {'token' : 'mockedToken'})
    
    result = client.post('/api/queue/login' , json={'user' : 'user' , 'password' : 'pass'})
    assert result.status_code == 200
    assert result.json['token'] == 'mockedToken'

def test_login_endpoint_missing_credentials(client):
    result = client.post('/api/queue/login' , json = {})
    assert result.status_code == 400
    assert result.json['message'] == 'Must provide credentials'