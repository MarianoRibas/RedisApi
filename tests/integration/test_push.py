import pytest
import os
import jwt
from pytest_mock import mocker
from conftest import client
from dotenv import load_dotenv
import fakeredis

validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")


def test_push_success(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request to add a message to the queue
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 201
    assert response.json['status'] == "ok"

def test_push_invalid(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request with no message
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code == 400

    #Request with wrong body
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"},  json={"wrong_key" : "Test Message"})
    assert response.status_code == 400

def test_push_exeption_redis (client, mocker):
    mocker.patch('services.services.r.rpush' , side_effect = Exception())
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']
    
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 500
    assert response.json['message'] == 'Connection error'

def test_push_exeption_service(client, mocker):
    mocker.patch('apis.push.push_item' , side_effect = Exception())
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']
    
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 500
    assert response.json['message'] == 'Internal error'

def test_push_no_token(client):
    #Request with no token
    response = client.post('/api/queue/push',json={'msg' : 'testMessage'} , headers={})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Must Provide a Token!'

def test_push_invalid_token(client):
    #Request with no token
    
    response = client.post('/api/queue/push',json={'msg' : 'testMessage'} , headers={'Authorization' : f'Bearer invalidToken'})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Invalid Token'

def test_push_expired_token(client, mocker):
    mocker.patch('services.services.jwt.decode' , side_effect = jwt.ExpiredSignatureError)

    #Request with expired token
    response = client.post('/api/queue/push',json={'msg' : 'testMessage'} , headers={'Authorization' : f'Bearer expiredToken'})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Expired Token'
    

