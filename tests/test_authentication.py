from conftest import client

def test_push_endpoint (client, path = 'push'):

#Request with no authentication
    response = client.post(f'api/queue/{path}')

    assert response.status_code == 401

#Request with wrong authentication
    response = client.post(f'api/queue/{path}' , headers={"Authentication" : f'Bearer WRONGTOKEN'})
    assert response.status_code == 401

