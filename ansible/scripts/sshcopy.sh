#!/bin/bash

sudo apt install sshpass dos2unix jq -y

if [ -f scripts/.env ]; then
    source scripts/.env
else
    echo "Файл .env не найден!"
    exit 1
fi

read -p "Сколько серверов? (по умолчанию 1): " COUNT
COUNT=${COUNT:-1}


VAULT_TOKEN="hvs.CAESIGtdkStXAvomud0nGMEQmlmxOTLzk7T-fLeEwUoaY6LRGh4KHGh2cy5YTVpyQWhCb2RubVRxTlF2b1lSeUs0d0c"
VAULT_ADDR="https://127.0.0.1:8200"

for ((i=1; i<=$COUNT; i++)); do

    SERVER="SSH_SERVER_${i}"
    SERVER_VALUE=${!SERVER}


    VAULT_RESPONSE=$(curl -s -k -H "X-Vault-Token: $VAULT_TOKEN" \
            "$VAULT_ADDR/v1/secrets/server${i}")

    PASSWORD_VALUE=$(echo "$VAULT_RESPONSE" | jq -r '.data.data.password')

    PASSWORD_VALUE=$(echo -e "$PASSWORD_VALUE")

    # Если есть и пользователь и сервер - работаем
    if [ -n "$SERVER_VALUE" ]; then
        echo "Сервер $i: $USER_VALUE@$SERVER_VALUE"

        # Если нет пароля - спрашиваем
        if [ -z "$PASSWORD_VALUE" ]; then
            read -s -p "Введите пароль для $USER_VALUE@$SERVER_VALUE: " PASSWORD_VALUE
            echo
        fi

        echo "Копируем ключ..."
        sshpass -p "$PASSWORD_VALUE" ssh-copy-id -i files/root_id_rsa root@$SERVER_VALUE 2>&1
        echo "Готово!"
        echo
    else
        echo "Пропускаем сервер $i - нет данных пользователя или сервера"
        echo
    fi
done