from pytest_mock import mocker
from services.services import queue_count


def test_count_success(mocker):
    mocker.patch('services.services.r.llen', return_value = 0)
    assert queue_count() == 0

def test_count_exception(mocker):
    mocker.patch('services.services.r.llen', side_effect = Exception('Error'))
    assert queue_count() == 'Connection error'