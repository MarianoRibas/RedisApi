from services.services import health_check
from pytest_mock import mocker



def test_healthCheck(mocker):
    mocker.patch('services.services.r.ping', return_value = True)
    assert health_check() == 'Redis database is healthy'
    mocker.patch('services.services.r.ping', side_effect = Exception('Error'))
    assert health_check() == 'Connection error'
