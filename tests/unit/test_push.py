from pytest_mock import mocker
from services.services import push_item


def test_push_ok(mocker):
    mocker.patch('services.services.r.rpush', return_value = 1)
    assert push_item('Test-message') == 1
    mocker.patch('services.services.r.rpush', side_effect = Exception('Error'))
    assert push_item('test-message') == 'Connection error'
    
    
     