from pytest_mock import mocker
from fakeredis import FakeStrictRedis
import pytest
from redis import Redis
from services.services import push_item



def test_push_ok(mocker):

    mocked_redis = mocker.Mock(spec = Redis())
    mocked_redis.rpush.return_value = 1
    result = push_item('Test-message', mocked_redis)

    assert result == 1
    
    