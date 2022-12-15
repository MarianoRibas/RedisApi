from pytest_mock import mocker
from services.services import push_item
from conftest import client

def test_push_endpoint_success(client, mocker):
    mocker.patch('apis.push.push_item', return_value = 1)
    mocker.patch('apis.push.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/push' , json={'msg' : 'Test-message'})
    assert result.status_code == 201
    assert result.json['status'] == 'ok'
    

def test_push_endpoint_invalid(client, mocker):
    mocker.patch('services.services.push_item', return_value = 1)
    mocker.patch('apis.push.verify_token_middleware', return_value = None )

    result = client.post('/api/queue/push' , json={})
    print(result)
    assert result.status_code == 400
    assert result.json['status'] == 'Must provide a message'

