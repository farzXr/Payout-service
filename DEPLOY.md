# Deploy проекта payout-service на production

Изначально я хотел использовать ansible, но я его только начал изучать, поэтому моих компетенций не хватило чтобы создать корректный playbook для скачивания всех зависимостей и role для поднятия gitlab-runner на prod, и я отказался от этой идеи. Поэтому будем делать по старинке - всё руками(

1. На dev-сервере создаём ssh ключ для подключения в prod-серверу без пароля
```commandline
ssh-keygen -t ed25519
```
2. Прокидываем его на prod-сервер, здесь нам нужен пароль от прода
```commandline
ssh-copy-id username@host
```
3. Подключаемся
```commandline
ssh username@host
```

4. Добавляем нашего пользователя в sudo, что не писать каждый раз пароль
```commandline
sudo visudo
#Добавляем в конец файла
username ALL=(ALL) NOPASSWD: ALL
```

5.Качаем git и docker, docker-compose
```commandline
1. sudo apt update -y
2. sudo apt install git -y
3. # Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

4. sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

6. Клонируем репозиторий
```commandline
git clone <repo_url>
cd payout-service
```

7. На gitlab получаем токен для cicd, создаем в проде .env в ./gitlab-runner и вставляем его туда 
```commandline
RUNNER_TOKEN=you-token
```

8. Поднимаем заранее настроенный gitlab-runner
```commandline
cd gitlab-runner
docker compose up -d --build
```

9. А дальше курим бамбук и всё отлаживаем)


ps.
gitlab-ci не отлажен, также как и gitlab-runner, я их просто написал для деплоя "на словах" как я их вижу


