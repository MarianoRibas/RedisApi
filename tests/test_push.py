from conftest import client
import os
from dotenv import load_dotenv

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")

def test_push(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    # Request authentication
    #test_authentication(client, 'push')

    #Request with no message
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code == 400

    #Request with wrong body
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"},  json={"wrong_key" : "Test Message"})
    assert response.status_code == 400
    
    #Request to add a message to the queue
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 201
    assert response.json['status'] == "ok"

