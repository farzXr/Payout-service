.PHONY: help create_ssl start_vault init_vault unseal_vault first_login enable_auth enable_secrets enable_audit write_policies write_user write_approle set_secrets setup

help:
	@echo "Использование:"
	@echo "  make                     - полная настройка vault (alias для setup)"
	@echo "  make help                - показать это сообщение"
	@echo "  make create_ssl          - создать ssl файлы для listener"
	@echo "  make start_vault         - запустить vault server"
	@echo "  make init_vault          - инициализировать vault (получить ключи и токен)"
	@echo "  make unseal_vault        - разархивировать vault с помощью ключей"
	@echo "  make first_login         - войти в vault с root токеном"
	@echo "  make enable_auth         - включить методы аутентификации"
	@echo "  make enable_secrets      - включить secrets engine"
	@echo "  make enable_audit        - включить аудит"
	@echo "  make write_policies      - записать политики доступа"
	@echo "  make write_user          - создать пользователя"
	@echo "  make write_approle       - создать AppRole"
	@echo "  make set_secrets         - записать необходимые"
	@echo "  make setup               - полная настройка vault (все шаги выше)"
	@echo ""
	@echo "Порядок работы:"
	@echo "  1. make create_ssl       # Создать SSL сертификаты"
	@echo "  2. make start_vault      # Запустить сервер"
	@echo "  3. make init_vault       # Инициализировать и получить ключи"
	@echo "  4. make unseal_vault     # Разархивировать vault"
	@echo "  5. make first_login      # Войти с root токеном"
	@echo "  6. make enable_auth      # Включить аутентификацию (userpass, approle)"
	@echo "  7. make enable_secrets   # Включить хранилище секретов"
	@echo "  8. make enable_audit     # Включить аудит"
	@echo "  9. make write_policies   # Создать политики (admin, developer, gitlab-runner)"
	@echo "  10. make write_user      # Создать пользователя"
	@echo "  11. make write_approle   # Создать AppRole"
	@echo "  12. make set_secrets     # Записать необходимые секреты"
	@echo "  Или просто: make setup   # Все шаги автоматически"

create_ssl: ./scripts/create-ssl.sh ./configs/tls
	chmod +x ./scripts/create-ssl.sh
	./scripts/create-ssl.sh

start_vault: ./scripts/start-vault.sh ./configs/server.hcl ./configs/listener.hcl ./configs/raft.hcl ./configs/telemetry.hcl ./configs/logs.hcl
	chmod +x ./scripts/start-vault.sh
	scripts/start-vault.sh

init_vault:
	vault operator init

unseal_vault: ./scripts/unseal.sh
	chmod +x ./scripts/unseal.sh
	./scripts/unseal.sh

first_login:
	@read -p "Введите root token (он был показан выше в выводе): " ROOT_TOKEN && \
	vault login $$ROOT_TOKEN

enable_audit:
    mkdir -p ./logs/audit.log
	vault audit enable file file_path=./logs/audit.log

enable_auth:
	vault auth enable userpass
	vault auth enable approle

enable_secrets:
	vault secrets enable -path=secrets -version=2 kv

write_policies: ./policies/admin.hcl ./policies/developer.hcl
	vault policy write admin ./policies/admin.hcl && \
	vault policy write developer ./policies/developer.hcl && \
	vault policy write gitlab-runner ./policies/gitlab-runner.hcl

write_approle: ./scripts/write_approle.sh
	chmod +x ./scripts/write_approle.sh
	./scripts/write_approle.sh

set_secrets: ./scripts/set-secrets.sh
	chmod +x ./scripts/set-secrets.sh
	./scripts/set-secrets.sh

write_user: ./scripts/write_user.sh
	chmod +x ./scripts/write_user.sh
	./scripts/write_user.sh

setup: init_vault unseal_vault first_login enable_auth enable_secrets enable_audit write_policies write_approle set_secrets write_user
	@echo "Настройка Vault завершена!"

default: setup