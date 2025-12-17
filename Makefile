.PHONY: help start stop restart clean logs test createsuperuser shell

help:
	@echo "Доступные команды:"
	@echo "  help           - Показать это сообщение"
	@echo "  start          - Поднять сервисы (docker compose up -d --build)"
	@echo "  stop           - Остановить сервисы (docker compose down)"
	@echo "  restart        - Перезапустить сервисы (docker compose restart)"
	@echo "  clean          - Остановить и удалить тома, очистить Docker (docker compose down -v && docker system prune -f)"
	@echo "  logs           - Смотреть логи (docker compose logs -f)"
	@echo "  test           - Запустить тесты в контейнере приложения"
	@echo "  createsuperuser- Создать суперпользователя Django в контейнере"
	@echo "  shell          - Открыть Django shell в контейнере"

start:
	docker compose up -d --build

stop:
	docker compose down

restart:
	docker compose restart

clean:
	docker compose down -v && docker system prune -f

logs:
	docker compose logs -f

test:
	docker exec -it app poetry run python manage.py test payouts

createsuperuser:
	docker exec -it app poetry run python manage.py createsuperuser

shell:
	docker exec -it app poetry run python manage.py shell