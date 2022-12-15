import pytest
from pytest_mock import mocker
from services.services import health_check
from conftest import client

@pytest.mark.parametrize('healthValue, expectedResult',[
    ('Redis database is healthy','Redis database is healthy'),
    ('Redis database is unhealthy','Redis database is unhealthy')
])
def test_healthCheck_endpoint(client, mocker, healthValue, expectedResult):
    mocker.patch('apis.healthCheck.health_check', return_value = healthValue)
    mocker.patch('apis.healthCheck.verify_token_middleware', return_value = None )
    
    result = client.post('/api/queue/healthCheck')
    assert result.status_code == 200
    assert result.json['message'] == expectedResult



