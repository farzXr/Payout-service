#!/bin/sh

echo "===Ключи смотреть чуть выше в выводе (не забываем копировать пробел вначале каждого ключа - это его неотъемлемая часть)==="

for i in 1 2 3
do
    echo -n "Введите ключ $i: "
    read key
    vault operator unseal $key
    echo ""
done

echo "Проверяем статус Vault..."
vault status