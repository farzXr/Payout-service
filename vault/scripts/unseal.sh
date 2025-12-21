#!/bin/bash

export VAULT_ADDR=https://127.0.0.1:8200

for i in 1 2 3
do
    echo -n "Введите ключ $i: "
    read key
    vault operator unseal $key
    echo ""
done

echo "Проверяем статус Vault..."
vault status