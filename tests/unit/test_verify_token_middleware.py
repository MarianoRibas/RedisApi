from services.services import verify_token_middleware
from services import services
from pytest_mock import MockerFixture

def test_verify_token_middleware_success(mocker : MockerFixture):
    mocker.patch('services.services.jwt.decode', return_value = 'OK')
    headers = {'Authorization' : 'Bearer token'}
    result = verify_token_middleware(headers)

    assert  not result

def test_verify_token_middleware_missing(mocker : MockerFixture):
    headers = {}
    result = verify_token_middleware(headers)
    
    assert  result[0] == 'Must Provide a Token!'

def test_verify_token_middleware_invalid(mocker : MockerFixture):
    headers = {'Authorization' : 'Bearer invalidToken'}
    result = verify_token_middleware(headers)
    
    assert  result[0] == 'Invalid Token'