from pytest_mock import mocker
from fakeredis import FakeStrictRedis
from services.services import pop_item

def test_pop(mocker):
    fake_redis = FakeStrictRedis()
    mocked_redis = mocker.Mock(spec = fake_redis)
    mocked_redis.lpop.return_value = 'Test-message'
    result = pop_item(r = mocked_redis)

    assert result == 'Test-message'

    

