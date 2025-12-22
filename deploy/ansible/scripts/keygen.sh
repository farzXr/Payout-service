#!/bin/bash

mkdir -p ~/.ssh

ssh-keygen -t rsa -b 4096 -f ~/.ssh/root_id_rsa -C "root@bootstrap" -N ""
echo "Ключ для root создан"

ssh-keygen -t ed25519 -f ~/.ssh/ansible_id_rsa -C "ansible@production" -N ""
echo "Ключ для ansible создан"

mkdir -p files

cp ~/.ssh/root_id_rsa files/
cp ~/.ssh/ansible_id_rsa files/

cp ~/.ssh/root_id_rsa.pub files/
cp ~/.ssh/ansible_id_rsa.pub files/

echo "Ключи скопированы в папку files"