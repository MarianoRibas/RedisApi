from pytest_mock import mocker
from fakeredis import FakeStrictRedis
from services.services import queue_count


def test_count(mocker):
    fake_redis = FakeStrictRedis()
    mocked_redis = mocker.Mock(spec = fake_redis)
    mocked_redis.llen.return_value = 0
    
    response = queue_count(r= mocked_redis)
    assert response == 0
    