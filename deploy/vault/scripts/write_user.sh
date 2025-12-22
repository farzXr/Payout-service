#!/bin/sh

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