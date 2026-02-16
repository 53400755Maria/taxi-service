"""Tests for order functionality."""
import pytest
import json
from app.server import app, generate_order_id


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_generate_order_id():
    """Test order ID generation."""
    order_id = generate_order_id()
    assert order_id.startswith('ORD-')
    assert len(order_id) > 10


def test_get_orders(client):
    """Test getting orders list."""
    response = client.get('/api/orders')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'orders' in data
