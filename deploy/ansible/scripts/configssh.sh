#!/bin/bash

# Если нет исходного файла - создаём пример
if [ ! -f "scripts/config-ssh" ]; then
    echo "Нет config-ssh..."
    exit 1
fi

mkdir -p ~/.ssh

if [ -f ~/.ssh/config ]; then
    echo "" >> ~/.ssh/config
    echo "# Добавлено $(date)" >> ~/.ssh/config
    cat scripts/config-ssh >> ~/.ssh/config
    echo "Добавил настройки в конец ~/.ssh/config"
else
    # Если файла нет - создаём новый
    cat scripts/config-ssh > ~/.ssh/config
    echo "Создал новый ~/.ssh/config"
fi

# Правильные права
chmod 600 ~/.ssh/config
chmod 700 ~/.ssh

echo "Готово!"