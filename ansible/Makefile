.PHONY: help all set_vars create_keys ssh_copy config_ssh install_requirements bootstrap_servers gitlab_runner boot_setup full_setup clean

help:
	@echo "Использование:"
	@echo "  make                        - создать ключи (по умолчанию, alias для create_keys)"
	@echo "  make help                   - показать эту справку"
	@echo ""
	@echo "Основные цели:"
	@echo "  make set_vars              - установить переменные из HashiCorp Vault"
	@echo "  make create_keys           - создать SSH ключи"
	@echo "  make ssh_copy              - скопировать ключи на серверы"
	@echo "  make config_ssh            - добавить хосты в конфиг SSH"
	@echo "  make install_requirements  - установить необходимые Ansible коллекции"
	@echo "  make bootstrap_servers     - произвести базовую настройку целевых серверов"
	@echo "  make gitlab_runner         - установить и настроить GitLab Runner"
	@echo "  make clean                 - удалить публичные ключи из files/"
	@echo ""
	@echo "Комплексные цели (рекомендуемый порядок выполнения):"
	@echo "  1. make set_vars           # Настроить переменные из Vault"
	@echo "  2. make create_keys        # Создать SSH ключи"
	@echo "  3. make ssh_copy           # Скопировать ключи на серверы"
	@echo "  4. make install_requirements # Установить зависимости Ansible"
	@echo "  5. make bootstrap_servers  # Базовая настройка серверов (включает config_ssh)"
	@echo "  6. make gitlab_runner      # Установка GitLab Runner"
	@echo ""
	@echo "Быстрые сценарии:"
	@echo "  make boot_setup            = create_keys + ssh_copy + install_requirements + bootstrap_servers"
	@echo "  make full_setup            = set_vars + boot_setup + gitlab_runner (полная настройка)"
	@echo ""
	@echo "Требования к Vault:"
	@echo "  Перед запуском убедитесь, что в HashiCorp Vault в движке kv есть секреты:"
	@echo "  1. secrets/gitlab/token-api (value=...) - токен GitLab с правами API"
	@echo "  2. secrets/server1 (password=...) - SSH пароль root для server1"
	@echo "  (запустите make set_vars для получения подробных инструкций)"

all: create_keys

set_vars: ./scripts/set_vars.sh ./group_vars/all
	chmod +x scripts/set_vars.sh
	./scripts/set_vars.sh
	@echo ""
	@echo "ВАЖНО: Убедитесь, что в HashiCorp Vault в движке kv есть следующие секреты:"
	@echo "  1. secrets/gitlab/token-api (value=...) - токен GitLab с правами API"
	@echo "  2. secrets/server1 (password=...) - SSH пароль root для server1"
	@echo "  3. secrets/server2 (password=...) - SSH пароль root для server2 (если используется)"

create_keys: scripts/keygen.sh
	chmod +x scripts/keygen.sh
	./scripts/keygen.sh

ssh_copy: scripts/sshcopy.sh files/root_id_rsa scripts/.env
	chmod +x scripts/sshcopy.sh
	./scripts/sshcopy.sh

config_ssh: scripts/configssh.sh scripts/config-ssh
	chmod +x scripts/configssh.sh
	./scripts/configssh.sh

install_requirements: requirements.yml
	ansible-galaxy collection install -r requirements.yml -p ./collections --force

bootstrap_servers: ./playbooks/bootstrap.yml ./roles/bootstrap/tasks/main.yml
	ansible-playbook ./playbooks/bootstrap.yml --tags first-setup && \
	ansible-playbook ./playbooks/bootstrap.yml --tags install

gitlab_runner: ./playbooks/runner.yml ./roles/gitlab-runner/tasks/main.yml ./group_vars/all/secrets.yml ./group_vars/all/vars.yml
	ansible-playbook ./playbooks/runner.yml

boot_setup: create_keys ssh_copy install_requirements bootstrap_servers

full_setup: set_vars boot_setup gitlab_runner
	@echo "Полная настройка завершена!"
	@echo "Все системы готовы к работе."

clean:
	rm -f files/*.pub
	@echo "Публичные ключи удалены из папки files"

default: create_keys