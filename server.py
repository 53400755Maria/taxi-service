from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import random
import string

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Папка для хранения заказов
ORDERS_FILE = 'orders.json'
DRIVERS_FILE = 'drivers.json'  # База водителей

# База данных водителей (в реальном проекте хранится в БД)
DEFAULT_DRIVERS = [
    {
        "id": "1",
        "name": "Иван Петров",
        "car": "Kia Rio 2020",
        "car_number": "А123БВ 777",
        "phone": "+7 (912) 345-67-89",
        "rating": 4.8,
        "status": "free",
        "coordinates": {"lat": 55.7558, "lng": 37.6176}
    },
    {
        "id": "2",
        "name": "Анна Сидорова",
        "car": "Hyundai Solaris 2021",
        "car_number": "Б456ГД 777",
        "phone": "+7 (923) 456-78-90",
        "rating": 4.9,
        "status": "free",
        "coordinates": {"lat": 55.7614, "lng": 37.6098}
    },
    {
        "id": "3",
        "name": "Сергей Иванов",
        "car": "Skoda Octavia 2019",
        "car_number": "В789ЕЖ 777",
        "phone": "+7 (934) 567-89-01",
        "rating": 4.7,
        "status": "free",
        "coordinates": {"lat": 55.7500, "lng": 37.6200}
    },
    {
        "id": "4",
        "name": "Мария Кузнецова",
        "car": "Toyota Camry 2022",
        "car_number": "Г012ЗИ 777",
        "phone": "+7 (945) 678-90-12",
        "rating": 5.0,
        "status": "free",
        "coordinates": {"lat": 55.7700, "lng": 37.6300}
    }
]

# Цены на тарифы
PRICES = {
    "economy": 150,
    "comfort": 250,
    "business": 400,
    "minivan": 500
}

# Загружаем сохраненные заказы
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохраняем заказы
def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# Загружаем водителей
def load_drivers():
    if os.path.exists(DRIVERS_FILE):
        with open(DRIVERS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return DEFAULT_DRIVERS
    else:
        # Создаем файл с водителями по умолчанию
        save_drivers(DEFAULT_DRIVERS)
        return DEFAULT_DRIVERS

# Сохраняем водителей
def save_drivers(drivers):
    with open(DRIVERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(drivers, f, ensure_ascii=False, indent=2)

# Генерация уникального ID заказа
def generate_order_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{timestamp}-{random_part}"

# Поиск ближайшего свободного водителя
def find_nearest_driver(order_coordinates=None):
    drivers = load_drivers()
    free_drivers = [d for d in drivers if d.get('status') == 'free']
    
    if not free_drivers:
        return None
    
    # В реальном приложении здесь поиск по координатам
    # Пока просто возвращаем случайного
    return random.choice(free_drivers)

# Расчет стоимости поездки
def calculate_price(car_type, distance_km=5):
    base_price = PRICES.get(car_type, 250)
    
    # Добавляем коэффициент за расстояние
    if distance_km > 10:
        return base_price + (distance_km - 10) * 20
    return base_price

# Статические файлы
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API endpoint для получения заказов
@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = load_orders()
    
    # Фильтрация по параметрам
    status = request.args.get('status')
    if status:
        orders = [o for o in orders if o.get('status') == status]
    
    limit = request.args.get('limit', type=int)
    if limit:
        orders = orders[:limit]
    
    return jsonify({
        'success': True,
        'count': len(orders),
        'orders': orders
    })

# API endpoint для получения конкретного заказа
@app.route('/api/order/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = load_orders()
    order = next((o for o in orders if o.get('id') == order_id), None)
    
    if order:
        return jsonify({
            'success': True,
            'order': order
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Заказ не найден'
        }), 404

# API endpoint для создания заказа
@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        
        # Валидация данных
        required_fields = ['from', 'to', 'phone', 'carType', 'payment']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Отсутствует поле {field}'
                }), 400
        
        # Находим водителя
        driver = find_nearest_driver()
        
        if not driver:
            return jsonify({
                'success': False,
                'error': 'Нет свободных водителей'
            }), 400
        
        # Рассчитываем цену
        price = calculate_price(data['carType'])
        
        # Обновляем статус водителя
        drivers = load_drivers()
        for d in drivers:
            if d['id'] == driver['id']:
                d['status'] = 'busy'
                break
        save_drivers(drivers)
        
        # Создаем заказ
        order = {
            'id': generate_order_id(),
            'created_at': datetime.now().isoformat(),
            'status': 'accepted',
            'driver': {
                'id': driver['id'],
                'name': driver['name'],
                'car': driver['car'],
                'car_number': driver['car_number'],
                'phone': driver['phone'],
                'rating': driver['rating']
            },
            'price': price,
            'estimated_arrival': random.randint(5, 15),  # минут
            'from_address': data['from'],
            'to_address': data['to'],
            'client_phone': data['phone'],
            'car_type': data['carType'],
            'payment_method': data['payment']
        }
        
        # Загружаем существующие заказы
        orders = load_orders()
        
        # Добавляем новый заказ
        orders.append(order)
        
        # Сохраняем обновленный список
        save_orders(orders)
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'driver': {
                'name': driver['name'],
                'car': driver['car'],
                'phone': driver['phone']
            },
            'price': price,
            'estimated_arrival': order['estimated_arrival'],
            'message': 'Заказ успешно создан'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# API endpoint для обновления статуса заказа
@app.route('/api/order/<order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.json
        orders = load_orders()
        
        # Находим и обновляем заказ
        order_found = False
        for order in orders:
            if order.get('id') == order_id:
                # Обновляем поля
                for key, value in data.items():
                    if key != 'id' and key != 'created_at':
                        order[key] = value
                
                order['updated_at'] = datetime.now().isoformat()
                
                # Если заказ отменен, освобождаем водителя
                if data.get('status') == 'cancelled' and 'driver' in order:
                    drivers = load_drivers()
                    for d in drivers:
                        if d['id'] == order['driver']['id']:
                            d['status'] = 'free'
                            break
                    save_drivers(drivers)
                
                order_found = True
                break
        
        if not order_found:
            return jsonify({
                'success': False,
                'error': 'Заказ не найден'
            }), 404
        
        save_orders(orders)
        
        return jsonify({
            'success': True,
            'message': 'Заказ обновлен'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# API для отмены заказа
@app.route('/api/order/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    try:
        orders = load_orders()
        
        for order in orders:
            if order.get('id') == order_id:
                if order['status'] in ['completed', 'cancelled']:
                    return jsonify({
                        'success': False,
                        'error': 'Заказ уже завершен или отменен'
                    }), 400
                
                # Освобождаем водителя
                if 'driver' in order:
                    drivers = load_drivers()
                    for d in drivers:
                        if d['id'] == order['driver']['id']:
                            d['status'] = 'free'
                            break
                    save_drivers(drivers)
                
                order['status'] = 'cancelled'
                order['cancelled_at'] = datetime.now().isoformat()
                order['cancel_reason'] = request.json.get('reason', 'Отменен клиентом')
                
                save_orders(orders)
                
                return jsonify({
                    'success': True,
                    'message': 'Заказ отменен'
                })
        
        return jsonify({
            'success': False,
            'error': 'Заказ не найден'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# API для получения статистики
@app.route('/api/stats', methods=['GET'])
def get_stats():
    orders = load_orders()
    
    if not orders:
        return jsonify({
            'success': True,
            'stats': {
                'total_orders': 0,
                'today_orders': 0,
                'completed_orders': 0,
                'cancelled_orders': 0,
                'avg_price': 0,
                'avg_response_time': '0 мин',
                'completion_rate': '0%'
            }
        })
    
    today = datetime.now().date().isoformat()
    today_orders = [o for o in orders if o['created_at'].startswith(today)]
    completed_orders = [o for o in orders if o.get('status') == 'completed']
    cancelled_orders = [o for o in orders if o.get('status') == 'cancelled']
    
    # Средняя стоимость
    prices = [o.get('price', 0) for o in orders if o.get('price')]
    avg_price = sum(prices) / len(prices) if prices else 0
    
    # Процент выполненных заказов
    completion_rate = (len(completed_orders) / len(orders)) * 100 if orders else 0
    
    stats = {
        'total_orders': len(orders),
        'today_orders': len(today_orders),
        'completed_orders': len(completed_orders),
        'cancelled_orders': len(cancelled_orders),
        'avg_price': round(avg_price, 2),
        'avg_response_time': '7 мин',  # В реальном приложении считаем из данных
        'completion_rate': f"{round(completion_rate, 1)}%"
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })

# API для получения списка водителей
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    drivers = load_drivers()
    
    # Фильтрация по статусу
    status = request.args.get('status')
    if status:
        drivers = [d for d in drivers if d.get('status') == status]
    
    return jsonify({
        'success': True,
        'count': len(drivers),
        'drivers': drivers
    })

# API для обновления статуса водителя
@app.route('/api/driver/<driver_id>/status', methods=['PUT'])
def update_driver_status(driver_id):
    try:
        data = request.json
        new_status = data.get('status')
        
        if new_status not in ['free', 'busy', 'offline']:
            return jsonify({
                'success': False,
                'error': 'Некорректный статус'
            }), 400
        
        drivers = load_drivers()
        
        for driver in drivers:
            if driver.get('id') == driver_id:
                driver['status'] = new_status
                driver['status_updated_at'] = datetime.now().isoformat()
                break
        
        save_drivers(drivers)
        
        return jsonify({
            'success': True,
            'message': 'Статус водителя обновлен'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# API для расчета стоимости
@app.route('/api/calculate-price', methods=['POST'])
def calculate_price_api():
    try:
        data = request.json
        car_type = data.get('carType', 'economy')
        distance = data.get('distance', 5)
        
        price = calculate_price(car_type, distance)
        
        return jsonify({
            'success': True,
            'price': price,
            'currency': 'RUB',
            'car_type': car_type,
            'distance': distance
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'taxi-order-service',
        'version': '1.0.0'
    })

# Очистка старых заказов (административный endpoint)
@app.route('/api/admin/cleanup', methods=['POST'])
def cleanup_old_orders():
    try:
        days = request.json.get('days', 30)  # Удалять заказы старше 30 дней
        orders = load_orders()
        
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        new_orders = []
        
        for order in orders:
            order_date = datetime.fromisoformat(order['created_at']).timestamp()
            if order_date > cutoff_date:
                new_orders.append(order)
        
        save_orders(new_orders)
        
        return jsonify({
            'success': True,
            'message': f'Удалено {len(orders) - len(new_orders)} старых заказов',
            'remaining': len(new_orders)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Создаем файлы если их нет
    if not os.path.exists(ORDERS_FILE):
        save_orders([])
    
    if not os.path.exists(DRIVERS_FILE):
        save_drivers(DEFAULT_DRIVERS)
    
    print("="*50)
    print("🚖 TAXI SERVICE SERVER")
    print("="*50)
    print(f"Сервер запущен на http://localhost:5000")
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📊 Доступные эндпоинты:")
    print("   GET  /                     - главная страница")
    print("   GET  /api/health            - проверка сервера")
    print("   GET  /api/orders            - список заказов")
    print("   GET  /api/orders?status=    - фильтр по статусу")
    print("   GET  /api/order/<id>        - конкретный заказ")
    print("   POST /api/order              - создать заказ")
    print("   PUT  /api/order/<id>         - обновить заказ")
    print("   POST /api/order/<id>/cancel  - отменить заказ")
    print("   GET  /api/stats              - статистика")
    print("   GET  /api/drivers            - список водителей")
    print("   POST /api/calculate-price    - расчет стоимости")
    print("="*50)
    
    # Запускаем сервер
    app.run(host='localhost', port=5000, debug=True)