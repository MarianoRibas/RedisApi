from fakeredis import FakeStrictRedis
import pytest
from controllers import pop_item
from app import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    context = flask_app.app_context()
    context.push()
    
    return flask_app

@pytest.mark.parametrize('message, expected_result',[
    ('Test1','Test1'),
    ('Test2','Test2'),
])
def test_pop(message, expected_result):
    fake_redis = FakeStrictRedis()
    fake_redis.lpush('queue:messages',message)

    result = pop_item(r = fake_redis)

    assert result.decode('utf-8') == expected_result

