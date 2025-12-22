
# Payout-service

REST API сервис для управления заявками на выплату средств с асинхронной обработкой через Celery.

## Требования

- Python 3.10+
- Django 4.2+
- Django REST Framework
- Celery + Redis
- PostgreSQL
- Docker + Docker Compose


## Prod - Читать DEPLOY.md
```commandline
make deploy
```

# Быстрый запуск с Docker
## Предварительные требования

- Docker и Docker Compose
- Git

## Шаги для запуска
1. Клонируем репозиторий и переходим в директорию проекта:

```commandline
git clone <repository-url>
cd payout-service
````

2. Запускаем сервисы:

```commandline
docker compose up -d --build
```

3. Проверяем, что все сервисы поднялись:

```commandline
docker compose ps
```

Вы должны увидеть `app`, `db`, `worker` и `task-broker` со статусом `Up` и остальные неважные нам сервисы для мониторинга.

## Проверка сервисов

- Проверка app, там мы должны увидеть что ASGI запустился на 0.0.0.0:8080
- Также там мы должны увидеть успешное выполнение миграций 
```commandline
docker logs app
```

- Проверка worker, там мы должны увидеть информацию об успешно запушенном worker
```commandline
docker logs worker
```

- Проверка task-broker, там в ответ мы должны получить сообщение "pong"
```commandline
docker exec -it task-broker redis-cli ping
```

- Проверять db не нужно, поскольку у него есть healthycheek, который использует app и автоматически проверяет

# API Endpoints

## Заявки на выплату
- GET /api/v1/payouts/ - список всех заявок
- GET /api/v1/payouts/{id}/ - детали заявки
- POST /api/v1/payouts/ - создание новой заявки
- PATCH /api/v1/payouts/{id}/ - обновление заявки
- DELETE /api/v1/payouts/{id}/ - удаление заявки

## Пример создания заявки

```commandline
curl -X POST http://localhost:8000/api/v1/payouts/ \
  -H "Content-Type: application/json" \
  -d '{
      "amount": "1500.75",
      "currency": "RUB",
      "recipient_details": {
        "account_holder": "Иван Иванов",
        "account_number": "40817810500000012345",
        "bank_name": "Тинькофф"
      },
      "description": "Выплата за январь"
  }'
```

## Тестирование API через Postman
Коллекция тестов наших API для запуска одной кнопкой:
- https://www.postman.com/ren484/workspace/payout-service/collection/42150353-989d3b22-3c7b-4953-b195-4d1be830f7bb?action=share&creator=42150353

## Документация к API

1. Swagger 
```commandline
{BASE_URL}/api/v1/docs
```
2. Redoc
```commandline
{BASE_URL}/api/v1/redoc/
```


ps. 
Всё в целом отлажено и должно корректно работать
---