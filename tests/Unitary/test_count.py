import pytest
from fakeredis import FakeStrictRedis
from controllers import queue_count

@pytest.mark.parametrize('message, expected_result',[
    ('Test1','Test1'),
    ('Test2','Test2'),
])
def test_count(message, expected_result):
    fake_redis = FakeStrictRedis()
    
    response = queue_count(r= fake_redis)
    assert response['status'] == 'ok'
    assert response['count'] == 0

    fake_redis.lpush('queue:messages',message)
    
    response = queue_count(r = fake_redis)
    assert response['count'] == 1
    