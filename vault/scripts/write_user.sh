#!/bin/bash

# Запрашиваем значения у пользователя
read -p "Введите имя пользователя: " username
read -p "Введите пароль: " password
read -p "Введите политику (по умолчанию developer. ): " policies
read -p "Введите TTL (по умолчанию: 1h): " ttl

# Устанавливаем значения по умолчанию
username=${username}
password=${password}
policies=${policies:-developer}
ttl=${ttl:-1h}

# Выполняем команду
vault write auth/userpass/users/"$username" \
  password="$password" \
  policies="$policies" \
  ttl="$ttl"