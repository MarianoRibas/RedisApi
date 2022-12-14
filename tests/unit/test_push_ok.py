from pytest_mock import mocker
from fakeredis import FakeStrictRedis, FakeServer
from services.services import push_item


def test_push_ok(mocker):
    mocker.patch('services.services.r.rpush', return_value = 1)
    assert push_item('sjlakdjaslkdjsa') == 1
    
    
    