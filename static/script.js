

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Скрипт загружен и готов к работе');

    // ===== ПОЛУЧАЕМ ССЫЛКИ НА ЭЛЕМЕНТЫ =====
    const orderForm = document.getElementById('orderForm');
    const carTypeSelect = document.getElementById('carType');
    const estimatedPrice = document.getElementById('estimatedPrice');
    const statusMessage = document.getElementById('statusMessage');
    const driverInfo = document.getElementById('driverInfo');
    const orderNowBtn = document.getElementById('orderNowBtn');
    const phoneInput = document.getElementById('phone');
    const fromInput = document.getElementById('from');
    const toInput = document.getElementById('to');

    // Проверяем, что все элементы найдены
    if (!orderForm) {
        console.error('❌ Форма заказа не найдена! Проверьте ID элементов в HTML');
        return;
    }

    console.log('✅ Все элементы формы найдены');

    // ===== БАЗА ДАННЫХ =====
    const drivers = [
        { name: "Иван Петров", car: "Kia Rio 2020", phone: "+7 (912) 345-67-89", rating: 4.8 },
        { name: "Анна Сидорова", car: "Hyundai Solaris 2021", phone: "+7 (923) 456-78-90", rating: 4.9 },
        { name: "Сергей Иванов", car: "Skoda Octavia 2019", phone: "+7 (934) 567-89-01", rating: 4.7 },
        { name: "Мария Кузнецова", car: "Toyota Camry 2022", phone: "+7 (945) 678-90-12", rating: 5.0 },
        { name: "Дмитрий Соколов", car: "Volkswagen Polo 2021", phone: "+7 (956) 789-01-23", rating: 4.6 },
        { name: "Елена Волкова", car: "Kia Optima 2022", phone: "+7 (967) 890-12-34", rating: 4.9 }
    ];

    const basePrices = {
        economy: 150,
        comfort: 250,
        business: 400,
        minivan: 500
    };

    // ===== ФУНКЦИИ ДЛЯ РАБОТЫ С ЦЕНОЙ =====
    function updatePrice() {
        if (!carTypeSelect || !estimatedPrice) return;

        const selectedCar = carTypeSelect.value;
        const price = basePrices[selectedCar] || 250;
        estimatedPrice.textContent = `${price}₽`;
        console.log(`💰 Цена обновлена: ${price}₽ (${selectedCar})`);
    }

    if (carTypeSelect) {
        carTypeSelect.addEventListener('change', updatePrice);
        console.log('✅ Слушатель изменения цены добавлен');
    }

    // ===== МАСКА ДЛЯ ТЕЛЕФОНА =====
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            let formattedValue = '';

            if (value.length > 0) {
                // Формат: +7 (999) 999-99-99
                formattedValue = '+7';
                if (value.length > 1) {
                    formattedValue += ' (' + value.substring(1, 4);
                }
                if (value.length >= 4) {
                    formattedValue += ') ' + value.substring(4, 7);
                }
                if (value.length >= 7) {
                    formattedValue += '-' + value.substring(7, 9);
                }
                if (value.length >= 9) {
                    formattedValue += '-' + value.substring(9, 11);
                }
            }

            e.target.value = formattedValue;
        });

        console.log('✅ Маска для телефона добавлена');
    }

    // ===== ВАЛИДАЦИЯ ФОРМЫ =====
    function validateForm(formData) {
        const errors = [];

        // Проверка адреса "Откуда"
        if (!formData.from || formData.from.trim().length < 3) {
            errors.push('Укажите корректный адрес отправления');
            if (fromInput) fromInput.classList.add('error');
        } else {
            if (fromInput) fromInput.classList.remove('error');
        }

        // Проверка адреса "Куда"
        if (!formData.to || formData.to.trim().length < 3) {
            errors.push('Укажите корректный адрес назначения');
            if (toInput) toInput.classList.add('error');
        } else {
            if (toInput) toInput.classList.remove('error');
        }

        // Проверка телефона
        const phoneDigits = formData.phone.replace(/\D/g, '');
        if (phoneDigits.length < 11) {
            errors.push('Введите корректный номер телефона (11 цифр)');
            if (phoneInput) phoneInput.classList.add('error');
        } else {
            if (phoneInput) phoneInput.classList.remove('error');
        }

        // Проверка способа оплаты
        const paymentElement = document.querySelector('input[name="payment"]:checked');
        if (!paymentElement) {
            errors.push('Выберите способ оплаты');
        }

        return {
            isValid: errors.length === 0,
            errors: errors,
            payment: paymentElement ? paymentElement.value : null
        };
    }

    // ===== ПОКАЗ УВЕДОМЛЕНИЙ =====
    function showNotification(message, type = 'info') {
        // Создаем элемент уведомления
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        // Выбираем иконку в зависимости от типа
        let icon = 'fa-info-circle';
        if (type === 'success') icon = 'fa-check-circle';
        if (type === 'error') icon = 'fa-exclamation-circle';
        if (type === 'warning') icon = 'fa-exclamation-triangle';

        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${icon}"></i>
                <span>${message}</span>
            </div>
        `;

        // Стили для уведомления
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            border-left: 4px solid ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : type === 'warning' ? '#f39c12' : '#3498db'};
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            font-weight: 500;
        `;

        document.body.appendChild(toast);

        // Удаляем через 3 секунды
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(toast)) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    // ===== ОТПРАВКА ЗАКАЗА НА СЕРВЕР =====
    async function sendOrderToServer(orderData) {
        try {
            console.log('📤 Отправка заказа на сервер:', orderData);

            const response = await fetch('/api/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderData)
            });

            const result = await response.json();
            console.log('📥 Ответ от сервера:', result);

            if (!response.ok) {
                throw new Error(result.error || `Ошибка сервера: ${response.status}`);
            }

            return result;

        } catch (error) {
            console.error('❌ Ошибка при отправке на сервер:', error);

            // Если сервер недоступен, используем локальный режим
            if (!navigator.onLine || error.message.includes('Failed to fetch')) {
                console.log('⚠️ Сервер недоступен, работа в локальном режиме');
                return {
                    success: true,
                    local_mode: true,
                    message: 'Заказ принят в локальном режиме'
                };
            }

            throw error;
        }
    }

    // ===== ПОИСК ВОДИТЕЛЯ =====
    function findDriver() {
        // Имитация поиска водителя
        return new Promise((resolve) => {
            setTimeout(() => {
                const randomDriver = drivers[Math.floor(Math.random() * drivers.length)];
                const arrivalTime = Math.floor(Math.random() * 10) + 5;
                resolve({ driver: randomDriver, arrivalTime });
            }, 1500);
        });
    }

    // ===== ОБНОВЛЕНИЕ ИНФОРМАЦИИ О ВОДИТЕЛЕ =====
    function updateDriverInfo(driver, arrivalTime) {
        const driverNameEl = document.getElementById('driverName');
        const driverCarEl = document.getElementById('driverCar');
        const driverPhoneEl = document.getElementById('driverPhone');
        const arrivalTimeEl = document.getElementById('arrivalTime');

        if (driverNameEl) driverNameEl.textContent = driver.name;
        if (driverCarEl) driverCarEl.textContent = driver.car;
        if (driverPhoneEl) driverPhoneEl.textContent = driver.phone;
        if (arrivalTimeEl) arrivalTimeEl.textContent = arrivalTime;

        // Добавляем рейтинг, если есть элемент
        const driverRatingEl = document.getElementById('driverRating');
        if (driverRatingEl && driver.rating) {
            driverRatingEl.textContent = `⭐ ${driver.rating}`;
        }
    }

    // ===== ОСНОВНАЯ ФУНКЦИЯ ОФОРМЛЕНИЯ ЗАКАЗА =====
    async function placeOrder(formData) {
        console.log('🚕 Начало оформления заказа:', formData);

        // Показываем статус "Поиск машины"
        if (statusMessage) {
            statusMessage.innerHTML = '🔍 <span class="searching">Ищем подходящую машину...</span>';
            statusMessage.style.animation = 'pulse 1.5s infinite';
        }

        if (driverInfo) {
            driverInfo.classList.add('hidden');
        }

        try {
            // Отправляем заказ на сервер
            const serverResponse = await sendOrderToServer(formData);

            // Ищем водителя
            const { driver, arrivalTime } = await findDriver();

            // Обновляем информацию о водителе
            updateDriverInfo(driver, arrivalTime);

            // Обновляем статус
            if (statusMessage) {
                statusMessage.innerHTML = '✅ <span class="found">Машина найдена!</span>';
                statusMessage.style.animation = 'none';
            }

            if (driverInfo) {
                driverInfo.classList.remove('hidden');
                driverInfo.style.animation = 'fadeInUp 0.5s ease';
            }

            // Показываем успешное уведомление
            showNotification(
                serverResponse.local_mode
                    ? '✅ Заказ принят (локальный режим)'
                    : `✅ Заказ №${serverResponse.order_id || '...'} успешно оформлен`,
                'success'
            );

            // Прокручиваем к статусу
            const orderStatus = document.getElementById('orderStatus');
            if (orderStatus) {
                orderStatus.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }

            // Сохраняем заказ в localStorage для истории
            saveOrderToLocalStorage({
                ...formData,
                driver: driver,
                arrivalTime: arrivalTime,
                timestamp: new Date().toISOString(),
                orderId: serverResponse.order_id || 'local-' + Date.now()
            });

        } catch (error) {
            console.error('❌ Ошибка при оформлении заказа:', error);

            if (statusMessage) {
                statusMessage.innerHTML = '❌ <span class="error">Ошибка при оформлении заказа</span>';
                statusMessage.style.animation = 'none';
            }

            showNotification('Не удалось оформить заказ. Попробуйте позже.', 'error');
        }
    }

    // ===== СОХРАНЕНИЕ ЗАКАЗА В ЛОКАЛЬНОЕ ХРАНИЛИЩЕ =====
    function saveOrderToLocalStorage(order) {
        try {
            // Получаем существующие заказы
            const savedOrders = JSON.parse(localStorage.getItem('taxi_orders') || '[]');

            // Добавляем новый заказ
            savedOrders.push(order);

            // Ограничиваем историю 20 заказами
            if (savedOrders.length > 20) {
                savedOrders.shift();
            }

            // Сохраняем
            localStorage.setItem('taxi_orders', JSON.stringify(savedOrders));
            console.log('💾 Заказ сохранен в localStorage');

        } catch (error) {
            console.warn('Не удалось сохранить заказ в localStorage:', error);
        }
    }

    // ===== ОБРАБОТЧИК ОТПРАВКИ ФОРМЫ =====
    if (orderForm) {
        orderForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('📝 Форма отправлена');

            // Получаем данные формы
            const formData = {
                from: fromInput?.value.trim() || '',
                to: toInput?.value.trim() || '',
                phone: phoneInput?.value.trim() || '',
                carType: carTypeSelect?.value || 'economy'
            };

            // Валидация
            const validation = validateForm(formData);

            if (!validation.isValid) {
                // Показываем все ошибки
                validation.errors.forEach(error => {
                    showNotification(error, 'warning');
                });
                return;
            }

            // Добавляем способ оплаты
            formData.payment = validation.payment;

            // Блокируем кнопку отправки
            const submitBtn = orderForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Оформление...';
            }

            // Оформляем заказ
            await placeOrder(formData);

            // Разблокируем кнопку
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Заказать такси';
            }
        });

        console.log('✅ Обработчик формы добавлен');
    }

    // ===== КНОПКА "ЗАКАЗАТЬ ТАКСИ" В ГЕРОЕ =====
    if (orderNowBtn) {
        orderNowBtn.addEventListener('click', function() {
            const orderSection = document.getElementById('order');
            if (orderSection) {
                orderSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Подсвечиваем форму
                if (orderForm) {
                    orderForm.style.animation = 'pulse 0.5s 2';
                    setTimeout(() => {
                        orderForm.style.animation = '';
                    }, 1000);
                }
            }
        });

        console.log('✅ Кнопка "Заказать такси" настроена');
    }

    // ===== МОБИЛЬНОЕ МЕНЮ =====
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');

    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            if (nav.style.display === 'block') {
                nav.style.display = 'none';
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                nav.style.display = 'block';
                mobileMenuBtn.innerHTML = '<i class="fas fa-times"></i>';
            }
        });

        // Закрытие меню при клике на ссылку
        document.querySelectorAll('.nav-list a').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    nav.style.display = 'none';
                    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                }
            });
        });

        console.log('✅ Мобильное меню настроено');
    }

    // ===== ИНИЦИАЛИЗАЦИЯ =====
    updatePrice();

    // Добавляем анимации в CSS, если их нет
    addAnimationStyles();

    console.log('✅ Инициализация завершена. Сервис готов к работе!');
});

// ===== ДОБАВЛЕНИЕ НЕДОСТАЮЩИХ СТИЛЕЙ =====
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }

        .searching {
            animation: pulse 1.5s infinite;
            display: inline-block;
        }

        .found {
            color: #27ae60;
            font-weight: bold;
        }

        .error {
            color: #e74c3c;
        }

        .form-group input.error,
        .form-group select.error {
            border-color: #e74c3c !important;
            animation: shake 0.3s ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .fa-spinner {
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;

    document.head.appendChild(style);
}

// ===== ТЕСТОВЫЕ ФУНКЦИИ ДЛЯ КОНСОЛИ =====
window.testOrder = function() {
    console.log('🧪 Запуск тестового заказа');

    const testData = {
        from: "ул. Пушкина, 10",
        to: "ул. Лермонтова, 5",
        phone: "+7 (999) 999-99-99",
        carType: "comfort",
        payment: "card"
    };

    // Заполняем форму тестовыми данными
    const fromInput = document.getElementById('from');
    const toInput = document.getElementById('to');
    const phoneInput = document.getElementById('phone');
    const carTypeSelect = document.getElementById('carType');
    const paymentCash = document.querySelector('input[value="cash"]');
    const paymentCard = document.querySelector('input[value="card"]');

    if (fromInput) fromInput.value = testData.from;
    if (toInput) toInput.value = testData.to;
    if (phoneInput) phoneInput.value = testData.phone;
    if (carTypeSelect) carTypeSelect.value = testData.carType;
    if (paymentCard) paymentCard.checked = true;

    console.log('✅ Форма заполнена тестовыми данными');

    // Отправляем форму
    const orderForm = document.getElementById('orderForm');
    if (orderForm) {
        orderForm.dispatchEvent(new Event('submit'));
    }
};

window.showOrders = function() {
    console.log('📋 Заказы из localStorage:');
    const orders = JSON.parse(localStorage.getItem('taxi_orders') || '[]');
    console.table(orders);
};

console.log('ℹ️ Для тестового заказа введите: testOrder()');
console.log('ℹ️ Для просмотра истории заказов: showOrders()');
