from fakeredis import FakeStrictRedis
import pytest
from controllers import pop_item

@pytest.mark.parametrize('message, expected_result',[
    ('Test1','Test1'),
    ('Test2','Test2'),
])
def test_pop(message, expected_result):
    fake_redis = FakeStrictRedis()
    fake_redis.lpush('queue:messages',message)

    result = pop_item(r = fake_redis)

    assert result.decode('utf-8') == expected_result

