# Taxi Service (Учебная практика)

## Описание проекта
Одностраничное веб-приложение (SPA) для заказа такси. Реализовано на Flask с использованием HTML-шаблонов и статики.

## Структура репозитория
- `app/` – основное приложение (маршруты, логика)
- `static/` – статические файлы (CSS, JS, изображения)
- `templates/` – HTML-шаблоны
- `tests/` – модульные тесты (pytest)
- `.github/workflows/` – CI/CD пайплайны

## Локальный запуск (без Docker)
```bash
cd app
pip install -r requirements.txt
flask run

## Локальный запуск (с Docker)
docker compose up --build

## Публичный URL развёрнутого приложения:
https://taxi-service-k8xw.onrender.com
