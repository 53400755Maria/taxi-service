import os
from flask import Flask, request, jsonify, send_from_directory
import json
import random
import string
from datetime import datetime

app = Flask(__name__,
            static_folder='../static',
            template_folder='../templates')

# Пути к файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS_FILE = os.path.join(BASE_DIR, 'orders.json')
DRIVERS_FILE = os.path.join(BASE_DIR, 'drivers.json')

# База данных водителей
DEFAULT_DRIVERS = [
    {"id": "1", "name": "Иван Петров", "car": "Kia Rio 2020",
     "phone": "+7 (912) 345-67-89", "rating": 4.8},
    {"id": "2", "name": "Анна Сидорова", "car": "Hyundai Solaris 2021",
     "phone": "+7 (923) 456-78-90", "rating": 4.9},
    {"id": "3", "name": "Сергей Иванов", "car": "Skoda Octavia 2019",
     "phone": "+7 (934) 567-89-01", "rating": 4.7},
    {"id": "4", "name": "Мария Кузнецова", "car": "Toyota Camry 2022",
     "phone": "+7 (945) 678-90-12", "rating": 5.0}
]

PRICES = {"economy": 150, "comfort": 250, "business": 400, "minivan": 500}


# Настройка CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def load_drivers():
    if os.path.exists(DRIVERS_FILE):
        with open(DRIVERS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return DEFAULT_DRIVERS
    else:
        with open(DRIVERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DRIVERS, f, ensure_ascii=False, indent=2)
        return DEFAULT_DRIVERS


def generate_order_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{timestamp}-{random_part}"


# Маршруты для статических файлов
@app.route('/')
def serve_index():
    return send_from_directory('../templates', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if path.endswith('.css'):
        return send_from_directory('../static', path)
    elif path.endswith('.js'):
        return send_from_directory('../static', path)
    return send_from_directory('../templates', path)


# API endpoints
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = load_orders()
    return jsonify({'success': True, 'count': len(orders), 'orders': orders})


@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        driver = random.choice(load_drivers())
        price = PRICES.get(data.get('carType', 'economy'), 250)

        order = {
            'id': generate_order_id(),
            'created_at': datetime.now().isoformat(),
            'status': 'accepted',
            'from_address': data.get('from'),
            'to_address': data.get('to'),
            'client_phone': data.get('phone'),
            'car_type': data.get('carType'),
            'payment_method': data.get('payment'),
            'price': price,
            'driver': driver,
            'estimated_arrival': random.randint(5, 15)
        }

        orders = load_orders()
        orders.append(order)
        save_orders(orders)

        return jsonify({
            'success': True,
            'order_id': order['id'],
            'driver': {'name': driver['name'], 'car': driver['car'],
                       'phone': driver['phone']},
            'price': price,
            'estimated_arrival': order['estimated_arrival']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    return jsonify({'success': True, 'count': len(load_drivers()),
                    'drivers': load_drivers()})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    orders = load_orders()
    today = datetime.now().date().isoformat()
    today_orders = [o for o in orders if o['created_at'].startswith(today)]
    prices = [o.get('price', 0) for o in orders]
    avg_price = sum(prices) / len(prices) if prices else 0

    return jsonify({
        'success': True,
        'stats': {
            'total_orders': len(orders),
            'today_orders': len(today_orders),
            'avg_price': round(avg_price, 2),
            'avg_response_time': '7 мин',
            'completed_orders': 0,
            'cancelled_orders': 0,
            'completion_rate': '0.0%'
        }
    })


@app.route('/api/calculate-price', methods=['POST'])
def calculate_price():
    data = request.json
    car_type = data.get('carType', 'economy')
    price = PRICES.get(car_type, 250)
    return jsonify({'success': True, 'price': price})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
