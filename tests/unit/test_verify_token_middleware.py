from services.services import verify_token_middleware
from pytest_mock import MockerFixture, mocker
import jwt
import pytest
from app import create_app


def test_verify_token_middleware_success(mocker : MockerFixture):
    mocker.patch('services.services.jwt.decode', return_value = 'OK')
    headers = {'Authorization' : 'Bearer token'}
    result = verify_token_middleware(headers)

    assert  not result


def test_verify_token_middleware_missing():
    headers = {}
    result = verify_token_middleware(headers)
    
    assert  result[0] == 'Must Provide a Token!'


def test_verify_token_middleware_invalid(mocker : MockerFixture):
    app = create_app()
    context = app.app_context() 
    context.push()  
    mocker.patch('services.services.jwt.decode', side_effect = jwt.DecodeError())
    headers = {'Authorization' : 'Bearer invalidToken'}
    result = verify_token_middleware(headers)     
    assert  result[0].json['msg'] == 'Invalid Token'


def test_verify_token_middleware_expired(mocker : MockerFixture):
    app = create_app()
    context = app.app_context() 
    context.push()  
    mocker.patch('services.services.jwt.decode', side_effect = jwt.ExpiredSignatureError())
    headers = {'Authorization' : 'Bearer expiredToken'}
    result = verify_token_middleware(headers)     
    assert  result[0].json['msg'] == 'Expired Token'
    