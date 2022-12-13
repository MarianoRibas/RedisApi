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
   
def test_push_ok():
    fake_redis = FakeStrictRedis()
    result = push_item('Test Message',r = fake_redis)
    assert result['status'] == 'ok'
    