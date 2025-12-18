.PHONY: help all create_keys ssh_copy setup clean

help:
	@echo "Использование:"
	@echo "  make                        - создать ключи (по умолчанию)"
	@echo "  make create_keys            - создать ключи"
	@echo "  make ssh_copy               - скопировать ключи на серверы"
	@echo "  make setup                  - создать ключи, скопировать их и настроить конфиг ssh"
	@echo "  make clean                  - удалить публичные ключи из files/"
	@echo "  make help                   - показать эту справку"
	@echo "  make config_ssh             - добавляет наши хосты в конфиг ssh"
	@echo "  make bootstrap_servers      - производит базовую настройку целевых серверов"
	@echo "  make install_requirements   - устанавливает необходимые модули"

all: create_keys

create_pass:
	@read -s -p "Введите пароль для Vault: " password && echo "$$password" > .vault_pass && chmod 600 .vault_pass
	@echo "Пароль сохранен в .vault_pass"

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
	ansible-galaxy collection install community.general -p ./collections --force

bootstrap_servers: ./playbooks/bootstrap.yml ./roles/bootstrap/tasks/main.yml
	ansible-playbook ./playbooks/bootstrap.yml --tags first-setup && \
	ansible-playbook ./playbooks/bootstrap.yml --tags install


setup: install_requirements create_keys ssh_copy bootstrap_servers

clean:
	rm -f files/*.pub
	@echo "Публичные ключи удалены из папки files"