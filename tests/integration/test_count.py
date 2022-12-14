from conftest import client
import os
from dotenv import load_dotenv

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")

def test_count(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    response = client.post('api/queue/count' , headers = {'Authorization' : f'Bearer {token}'})
    previousQueueSize = int(response.json['count'])
    
    client.post('api/queue/push' , headers={'Authorization' : f'Bearer {token}'} , json={'msg' : 'TestMessage'})
    
    response = client.post('api/queue/count' , headers = {'Authorization' : f'Bearer {token}'})
    currentQueueSize = int(response.json['count'])

    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    assert  currentQueueSize == previousQueueSize + 1

