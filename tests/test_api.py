"""Tests for API endpoints."""
import pytest
import json
from app.server import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'


def test_create_order(client):
    """Test creating an order."""
    order_data = {
        'from': 'ул. Тестовая, 1',
        'to': 'ул. Проверочная, 2',
        'phone': '+7 (999) 999-99-99',
        'carType': 'economy',
        'payment': 'cash'
    }
    response = client.post('/api/order', json=order_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
