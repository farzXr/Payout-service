#!/bin/bash

if [ ! -f ~/.ssh/root_id_rsa ] && [ ! -f ./files/root_id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/root_id_rsa -C "root@bootstrap" -N ""
    echo "Ключ для root создан"
else
    echo "Ключ для root уже существует"
fi

# Создаем ключ для ansible (если его нет)
if [ ! -f ~/.ssh/ansible_id_rsa ] && [ ! -f ./files/ansible_id_rsa ]; then
    ssh-keygen -t ed25519 -f ~/.ssh/ansible_id_rsa -C "ansible@production" -N ""
    echo "Ключ для ansible создан"
else
    echo "Ключ для ansible уже существует"
fi

# Создаем папку files
mkdir -p files

# Копируем ключи
cp ~/.ssh/root_id_rsa files/
cp ~/.ssh/ansible_id_rsa files/

cp ~/.ssh/root_id_rsa.pub files/
cp ~/.ssh/ansible_id_rsa.pub files/

echo "Ключи скопированы в папку files"