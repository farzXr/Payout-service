#!/bin/sh

ENV_FILE="./../ansible/scripts/.env"

vault write auth/userpass/users/need-script \
  password=123 \
  policies=admin \
  ttl=1440


USER_TOKEN=$(vault write -format=json auth/userpass/login/need-script \
      password=123 | jq -r '.auth.client_token')


echo "Токен получен: ${USER_TOKEN:0:20}..."

cat > "$ENV_FILE" << EOF
HASHICORP_VAULT_TOKEN=$USER_TOKEN
EOF



echo "Первым лучше создать админа"

read -p "Введите имя пользователя: " username
read -p "Введите пароль: " password
read -p "Введите политику (на данный момент есть developer/admin): " policies
read -p "Введите TTL (по умолчанию: 1h): " ttl

username=${username}
password=${password}
policies=${policies:-developer}
ttl=${ttl:-1h}

vault write auth/userpass/users/"$username" \
  password="$password" \
  policies="$policies" \
  ttl="$ttl"

vault login -method=userpass username=${username} password=${password}