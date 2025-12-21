#!/bin/bash

read -p "Введите ssh пароль от root от целевого сервера" pass

vault kv put secrets/server1 password="$pass"

read -p "Введите access token gitlab-аккаунта с правами api" token

vault kv put secrets/gitlab/token-access value="$token"

echo "Секреты успешно сохранены в Vault!"

