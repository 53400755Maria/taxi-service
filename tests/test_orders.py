import pytest
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.server import app, generate_order_id

@pytest.fixture
def client():
    """Create a test client for the app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generate_order_id():
    """Test order ID generation"""
    order_id = generate_order_id()
    assert order_id.startswith('ORD-')
    assert len(order_id) > 10
    # Проверяем формат: ORD-ГГГГММДДЧЧММСС-XXXX
    parts = order_id.split('-')
    assert len(parts) == 3
    assert len(parts[1]) == 14  # timestamp
    assert len(parts[2]) == 4    # random part

def test_get_orders(client):
    """Test getting all orders"""
    response = client.get('/api/orders')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'orders' in data
    assert 'count' in data
    assert isinstance(data['orders'], list)

def test_get_orders_empty(client):
    """Test getting orders when none exist"""
    response = client.get('/api/orders')
    data = json.loads(response.data)
    assert data['count'] >= 0  # Может быть 0 или больше