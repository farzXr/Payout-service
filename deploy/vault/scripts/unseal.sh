#!/bin/sh

echo "===Ключи смотреть чуть выше в выводе==="

for i in 1 2 3
do
    echo -n "Введите ключ $i: "
    read key
    vault operator unseal $key
    echo ""
done

echo "Проверяем статус Vault..."
vault status