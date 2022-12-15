from services.services import authenticate
from pytest_mock import mocker



def test_authenticate_success(mocker):
    mocker.patch.dict('os.environ',{'USERNAME' : 'validUsername', 'PASSWORD' : 'validPassword'})
    
    result = authenticate('validUsername','validPassword')
    assert result == True

def test_authenticate_fail(mocker):
    mocker.patch.dict('os.environ',{'USERNAME' : 'validUsername', 'PASSWORD' : 'validPassword'})
    
    result = authenticate('wrongUsername','wrongPassword')
    assert result == False
