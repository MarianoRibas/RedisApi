from pytest_mock import mocker
from services.services import pop_item


def test_pop_success(mocker):
    mocker.patch('services.services.r.lpop', return_value = b'Mocked-message')
    assert pop_item() == 'Mocked-message'
  

def test_pop_exception(mocker):
    mocker.patch('services.services.r.lpop', side_effect = Exception('Error'))
    assert pop_item() == 'Connection error'
