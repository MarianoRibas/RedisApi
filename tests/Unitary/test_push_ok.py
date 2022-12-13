from fakeredis import FakeStrictRedis
import pytest
import json
from controllers import push_item
from app import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    context = flask_app.app_context()
    context.push()
    
    return flask_app

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
    