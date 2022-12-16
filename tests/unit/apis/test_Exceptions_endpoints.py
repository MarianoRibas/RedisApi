import pytest
from pytest_mock import mocker
from services.services import pop_item, push_item, queue_count, health_check
from conftest import client

@pytest.mark.parametrize('endpoint, service',[
    ('push','push_item'),
    ('pop','pop_item'),
    ('healthCheck','health_check'),
    ('count', 'queue_count')
])
def test_exceptions(client, mocker,endpoint,service):
    mocker.patch(f'apis.{endpoint}.{service}', return_value = 'Connection error')
    mocker.patch(f'apis.{endpoint}.verify_token_middleware', return_value = None )
    if endpoint == 'push':
        result = client.post('/api/queue/push' , json={'msg' : 'Test-message'})
    else:
        result = client.post(f'/api/queue/{endpoint}')
    print(result)
    assert result.status_code == 500
    assert result.json['message'] == 'Connection error'

@pytest.mark.parametrize('endpoint, service',[
    ('push','push_item'),
    ('pop','pop_item'),
    ('healthCheck','health_check'),
    ('count', 'queue_count')
])
def test_unexpected_exceptions(client, mocker,endpoint,service):
    mocker.patch(f'apis.{endpoint}.{service}', side_effect = Exception())
    mocker.patch(f'apis.{endpoint}.verify_token_middleware', return_value = None )
    if endpoint == 'push':
        result = client.post('/api/queue/push' , json={'msg' : 'Test-message'})
    else:
        result = client.post(f'/api/queue/{endpoint}')
    assert result.status_code == 500
    assert result.json['message'] == 'Internal error'