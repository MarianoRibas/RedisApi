import pytest
from conftest import client

#Request with no authentication
@pytest.mark.parametrize("test_input, expected_result", [
    ('push',401),
    ('pop',401),
    ('size',401),
    ('checkHealth',401)
])
def test_authentication_with_no_authentication (client, test_input, expected_result):
    response = client.post(f'api/queue/{test_input}')
    assert response.status_code == expected_result



#Request with wrong authentication
@pytest.mark.parametrize("test_input, expected_result", [
    ('push',401),
    ('pop',401),
    ('count',401),
    ('healthCheck',401)
])
def test_authentication_with_no_authentication (client, test_input, expected_result):
    response = client.post(f'api/queue/{test_input}' , headers={"Authentication" : f'Bearer WRONGTOKEN'})
    
    assert response.status_code == expected_result

    response = client.post(f'api/queue/{test_input}' , headers={"Authentication" : " "})
    
    assert response.status_code == expected_result

    



