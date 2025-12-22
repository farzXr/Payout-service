#!/bin/sh

# Создаем директорию для сертификатов
mkdir -p ./configs/tls

# Генерируем SSL сертификат
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout ./configs/tls/vault.key -out ./configs/tls/vault.crt \
  -subj "/CN=localhost" -days 365 -addext "subjectAltName=IP:127.0.0.1"

# В Alpine правильный путь для ca-certificates
# Файлы должны быть с расширением .crt
mkdir -p /usr/local/share/ca-certificates/

# Копируем сертификат с правильным именем
cp ./configs/tls/vault.crt /usr/local/share/ca-certificates/vault.crt

# Обновляем список доверенных сертификатов
# В Alpine это делается так:
update-ca-certificates