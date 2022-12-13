from conftest import client
import os
from dotenv import load_dotenv

secretKey = os.getenv("SECRETKEY")
validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")

def test_pop(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request authentication
    #test_authentication(client, 'pop')

    #Request to pop a message from the queue



