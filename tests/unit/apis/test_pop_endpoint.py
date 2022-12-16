from pytest_mock import mocker
from services.services import pop_item
from conftest import client

def test_pop_endpoint_success(client, mocker):
    mocker.patch('apis.pop.pop_item', return_value = 'Test-message-popped')
    mocker.patch('apis.pop.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/pop')
    assert result.status_code == 200
    assert result.json['status'] == 'ok'
    assert result.json['message'] == 'Test-message-popped'

def test_pop_endpoint_no_item(client, mocker):
    mocker.patch('apis.pop.pop_item', return_value = None)
    mocker.patch('apis.pop.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/pop')
    assert result.status_code == 200
    assert result.json['message'] == 'No items to pop'



