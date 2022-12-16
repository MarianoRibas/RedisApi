from conftest import client
import os
from dotenv import load_dotenv

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")

def test_pop_success(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request to add a message to the queue
    client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})




