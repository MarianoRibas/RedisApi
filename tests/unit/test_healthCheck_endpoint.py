from pytest_mock import mocker
from services.services import health_check
from conftest import client

def test_healthCheck_endpoint_healthy(client, mocker):
    mocker.patch('apis.healthCheck.health_check', return_value = 'Redis database is healthy')
    mocker.patch('apis.healthCheck.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/healthCheck')
    assert result.status_code == 200
    assert result.json['message'] == 'Redis database is healthy'

def test_healthCheck_endpoint_unhealthy(client, mocker):
    mocker.patch('apis.healthCheck.health_check', return_value = 'Redis database is unhealthy')
    mocker.patch('apis.healthCheck.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/healthCheck')
    assert result.status_code == 200
    assert result.json['message'] == 'Redis database is unhealthy'