# tests/test_app.py

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/kyc')
    assert response.status_code == 200

def test_invalid_route(client):
    response = client.get('/kyc1')
    assert response.status_code == 404


    
