from pytest_mock import mocker
from services.services import pop_item
from conftest import client

def test_count_endpoint_success(client, mocker):
    mocker.patch('apis.count.queue_count', return_value = 1)
    mocker.patch('apis.count.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/count')
    assert result.status_code == 200
    assert result.json['status'] == 'ok'

def test_count_endpoint_exception(client, mocker):
    mocker.patch('apis.count.queue_count', return_value = 'Connection error')
    mocker.patch('apis.count.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/count')
    assert result.status_code == 500
    assert result.json['message'] == 'Connection error'

def test_count_endpoint_unexpected_exception(client, mocker):
    mocker.patch('apis.count.queue_count', side_effect = Exception())
    mocker.patch('apis.count.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/count')
    assert result.status_code == 500
    assert result.json['message'] == 'Internal error'