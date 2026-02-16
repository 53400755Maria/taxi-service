import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'timestamp' in data

def test_create_order(client):
    """Test creating a new order"""
    order_data = {
        'from': 'ул. Тестовая, 1',
        'to': 'ул. Проверочная, 2',
        'phone': '+7 (999) 999-99-99',
        'carType': 'economy',
        'payment': 'cash'
    }
    
    response = client.post('/api/order', 
                          json=order_data,
                          content_type='application/json')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'order_id' in data
    assert 'driver' in data
    assert data['price'] == 150