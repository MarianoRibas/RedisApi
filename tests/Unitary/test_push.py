from fakeredis import FakeStrictRedis
import pytest
from controllers import push_item



@pytest.mark.parametrize('message, expected_result',[
    ('Test msg 1','Test msg 1'),
    (1,'1'),
    ([],'[]'),
])   
def test_push_ok(message, expected_result):
    fake_redis = FakeStrictRedis()
    result = push_item(message,r = fake_redis)
    pushedItem = fake_redis.lpop('queue:messages')

    assert result['status'] == 'ok'
    assert pushedItem.decode('utf-8') == expected_result
    