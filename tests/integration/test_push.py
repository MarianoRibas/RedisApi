import pytest
import os
import jwt
from pytest_mock import mocker
from conftest import client
from dotenv import load_dotenv
from fakeredis import FakeStrictRedis

validUsername = os.getenv("USERNAME")
validPassword = os.getenv("PASSWORD")


def test_controller_success(client, mocker):
    mocker.patch('services.services.get_redis' , return_value = FakeStrictRedis())
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request to add a message to the queue
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 201
    assert response.json['status'] == "ok"

    #Request to count messages in the queue
    response = client.post('/api/queue/count' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 200
    assert response.json['status'] == "ok"
    assert response.json['count'] == 1

    #Request to pop message from the queue
    response = client.post('/api/queue/pop' , headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    assert response.json['message'] == 'Test Message'

    #Request to check redis healthy
    response = client.post('/api/queue/healthCheck' , headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json['message'] == 'Redis database is healthy'


def test_push_invalid(client):
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']

    #Request with no message
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code == 400

    #Request with wrong body
    response = client.post('/api/queue/push' , headers={"Authorization" : f"Bearer {token}"},  json={"wrong_key" : "Test Message"})
    assert response.status_code == 400



@pytest.mark.parametrize('redisMethod, endpoint', [
    ('rpush' , 'push'),
    ('lpop', 'pop'),
    ('llen', 'count'),
    ('ping', 'healthCheck')
])
def test__exeptions_redis (client, mocker, redisMethod, endpoint):
    mocker.patch(f'services.services.r.{redisMethod}' , side_effect = Exception())
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']
    
    response = client.post(f'/api/queue/{endpoint}' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 500
    assert response.json['message'] == 'Connection error'


@pytest.mark.parametrize('service, endpoint', [
    ('push_item' , 'push'),
    ('pop_item', 'pop'),
    ('queue_count', 'count'),
    ('health_check', 'healthCheck')
])
def test_push_exeption_service(client, mocker, service, endpoint):
    mocker.patch(f'apis.{endpoint}.{service}' , side_effect = Exception())
    token = client.post('api/queue/login', json = {"user" : validUsername , "password" : validPassword})
    token = token.json['token']
    
    response = client.post(f'/api/queue/{endpoint}' , headers={"Authorization" : f"Bearer {token}"}, json={"msg" : "Test Message"})
    assert response.status_code == 500
    assert response.json['message'] == 'Internal error'


@pytest.mark.parametrize('endpoint', [
    ('push'),
    ('pop'),
    ('count'),
    ('healthCheck')
])
def test_push_no_token(client, endpoint):
    #Request with no token
    response = client.post(f'/api/queue/{endpoint}',json={'msg' : 'testMessage'} , headers={})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Must Provide a Token!'


@pytest.mark.parametrize('endpoint', [
    ('push'),
    ('pop'),
    ('count'),
    ('healthCheck')
])
def test_push_invalid_token(client,endpoint):
    #Request with no token
    response = client.post(f'/api/queue/{endpoint}',json={'msg' : 'testMessage'} , headers={'Authorization' : f'Bearer invalidToken'})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Invalid Token'


@pytest.mark.parametrize('endpoint', [
    ('push'),
    ('pop'),
    ('count'),
    ('healthCheck')
])
def test_push_expired_token(client, mocker, endpoint):
    mocker.patch('services.services.jwt.decode' , side_effect = jwt.ExpiredSignatureError)

    #Request with expired token
    response = client.post(f'/api/queue/{endpoint}',json={'msg' : 'testMessage'} , headers={'Authorization' : f'Bearer expiredToken'})
    
    assert response.status_code == 401
    assert response.json['msg'] == 'Expired Token'
    

