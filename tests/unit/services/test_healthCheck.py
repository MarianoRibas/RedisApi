from services.services import health_check
from pytest_mock import mocker



def test_healthCheck_healthy(mocker):
    mocker.patch('services.services.r.ping', return_value = True)
    assert health_check() == 'Redis database is healthy'

def test_healthCheck_unhealthy(mocker):
    mocker.patch('services.services.r.ping', return_value = False)
    assert health_check() == 'Redis database is unhealthy'

def test_healthCheck_exception(mocker):
    mocker.patch('services.services.r.ping', side_effect = Exception('Error'))
    assert health_check() == 'Connection error'
