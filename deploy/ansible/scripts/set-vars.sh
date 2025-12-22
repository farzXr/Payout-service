#!/bin/bash
mkdir -p ./group_vars/all

VARS_FILE="./group_vars/all/vars.yml"
SECRETS_FILE="./group_vars/all/secrets.yml"
VAULT_PASS_FILE=".vault_pass"
ENV_FILE="./scripts/.env"


echo "=== Создание файла vars.yml ==="
read -p "Введите значение для gitlab_project_slug (например: farzXr%2Fpayout-service): " gitlab_slug
cat >> "$VARS_FILE" << EOF
gitlab_project_slug: $gitlab_slug
EOF
echo "Файл $VARS_FILE создан успешно."

echo ""
echo "=== Настройка пароля для ansible-vault ==="
read -s -p "Введите пароль для ansible-vault: " vault_password
echo "$vault_password" > "$VAULT_PASS_FILE"
chmod 600 "$VAULT_PASS_FILE"
echo "Пароль сохранен в $VAULT_PASS_FILE"

echo ""
echo "=== Шифрование файла secrets.yml ==="
ansible-vault encrypt "$SECRETS_FILE" --encrypt-vault-id=default --vault-password-file="$VAULT_PASS_FILE"

echo ""
echo "=== Создание файла .env ==="
read -p "Введите ip целевого сервера: " ip_server
cat >> "$ENV_FILE" << EOF
SSH_SERVER_1=$ip_server
EOF
cat >> "$VARS_FILE" << EOF
ip_server_1: $ip_server
EOF
echo "Файл $ENV_FILE создан успешно."