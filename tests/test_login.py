import jwt
from conftest import validUsername, validPassword, secretKey
def test_login_endpoint(client):
    # Request with correct credentials
    response = client.post("/api/queue/login", json={
        "user" : validUsername,
        "password" : validPassword
    })
    
    assert response.status_code == 200
    assert 'token' in response.json
    
    if response.status_code == 200:
        token = response.json['token']
        decoded = jwt.decode(token,secretKey, algorithms=['HS256'])
        assert decoded['user'] == validUsername


    #Request with invalid credentials
    response = client.post("/api/queue/login", json={
        "user":"1",
        "password":"12"
    })

    assert response.status_code == 401
    assert response.json["message"] == 'Invalid credentials'


    #Request with missing credentials
    response = client.post("/api/queue/login", json={"user" : "testUser1"})
    
    assert response.status_code == 400
    assert response.json['message'] == 'Must provide credentials'

    #Request with no credentials
    response = client.post("/api/queue/login")
    
    assert response.status_code == 400
    assert response.json == None