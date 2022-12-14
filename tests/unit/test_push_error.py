from pytest_mock import mocker
from fakeredis import FakeStrictRedis, FakeServer
from services.services import push_item


def test_push_ok(mocker):

    mocker.patch('services.services.r.rpush', side_effect = 1)
    assert push_item('test-message') == 'Connection error'