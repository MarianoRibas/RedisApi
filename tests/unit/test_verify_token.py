from pytest_mock import MockerFixture
from services.services import verify_token
from app import create_app
import jwt

def test_verify_token_success(mocker : MockerFixture):
    mocker.patch('services.services.jwt.decode', return_value = 'Ok')
    
    result = verify_token('test-token')
    assert not result


def test_verify_token_middleware_invalid(mocker : MockerFixture):
    app = create_app()
    context = app.app_context() 
    context.push()  
    mocker.patch('services.services.jwt.decode', side_effect = jwt.DecodeError())
    headers = {'Authorization' : 'Bearer invalidToken'}
    result = verify_token(headers)     
    assert  result[0].json['msg'] == 'Invalid Token'


def test_verify_token_middleware_expired(mocker : MockerFixture):
    app = create_app()
    context = app.app_context() 
    context.push()  
    mocker.patch('services.services.jwt.decode', side_effect = jwt.ExpiredSignatureError())
    headers = {'Authorization' : 'Bearer expiredToken'}
    result = verify_token(headers)     
    assert  result[0].json['msg'] == 'Expired Token'

