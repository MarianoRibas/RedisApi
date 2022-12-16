from services.services import login
from pytest_mock import mocker

def test_login_success (mocker):
    mocker.patch('services.services.authenticate', return_value = True)
    mocker.patch('services.services.expire_time', return_value = 12345432)
    mocker.patch('services.services.jwt.encode', return_value = 'encodedToken')

    credentials = {
        'user' : 'validUsername',
        'password' : 'validPassword'
    }
    result = login(credentials)
    print(result)
    
    assert result['token'] == 'encodedToken'

def test_login_invalid_credentials(mocker):
    mocker.patch('services.services.authenticate', return_value = False)
    mocker.patch('services.services.expire_time', return_value = 12345432)
    

    credentials = { 'user' : '', 'password' : '' } 
    result = login(credentials)
    
    assert result['message'] == 'Invalid credentials'

def test_login_missing_credentials(mocker):
    credentials = {} 
    result = login(credentials)
    assert result['message'] == 'Must provide credentials'
