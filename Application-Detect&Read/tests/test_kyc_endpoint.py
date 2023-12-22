# tests/test_kyc_endpoint.py

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_kyc_endpoint_with_recto_only(client):
    recto_path = 'C:/Users/rimba/Desktop/293.jpg'
    with open(recto_path, 'rb') as recto_file:
        response = client.post('/kyc_v2', data={'recto_image': (recto_file, '293.jpg')})
    
    assert response.status_code == 200
    assert b'ID Image' in response.data  

def test_kyc_endpoint_with_both_images(client):
    recto_path = 'C:/Users/rimba/Desktop/293.jpg'
    verso_path = 'C:/Users/rimba/Desktop/380.jpg'
    
    with open(recto_path, 'rb') as recto_file, open(verso_path, 'rb') as verso_file:
        response = client.post('/kyc_v2', data={'recto_image': (recto_file, '293.jpg'),
                                                 'verso_image': (verso_file, '380.jpg')})
    
    assert response.status_code == 200
    assert b'ID Image' in response.data  



    
