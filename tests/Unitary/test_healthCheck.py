import pytest
import fakeredis 
from controllers import health_check

def test_health_check ():
    server = fakeredis.FakeServer()
    server.connected = False
    r = fakeredis.FakeStrictRedis( server = server)

    result = health_check(r = r)

    assert result == 'Connection error'
