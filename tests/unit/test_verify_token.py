from pytest_mock import MockerFixture
from services.services import verify_token


def test_verify_token(mocker : MockerFixture):
    mocker.patch('services.services.jwt.decode', return_value = 'Ok')
    
    result = verify_token('test-token')
    assert not result

def test_verify_token(mocker : MockerFixture):
    mocker.patch('services.services.jwt.decode', return_value = 'Ok')
    
    result = verify_token('test-token')
    assert not result

