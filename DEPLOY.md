# Deploy проекта payout-service на production

1. Я использовал ansible для подготовки целевого сервера к развёртыванию на нём payout-service и cicd.

2. Для секретов использовал HahsiCorp Vault (пароль от целевого сервера/access-token от gitlab/...).

3. Я организовал их docker-compose для удобства переносимости этой системы автоматизированного развёртывания.

## Всё очень просто

- Для запуска подготовки целевого сервера к развёртыванию
```commandline
make deploy
```

- Для перенастройки целевого сервера
```commandline
make reset_deploy
```

## make deploy

Необходимо будет:

### setup vault
1. Разблокировать после запуска vault тремя ключами (они будут в терминале, чуть выше просьбы ввода)
2. Авторизироваться в vault под root для начальной настройки (токен будет в том же месте, где и ключи для разлока)
```commandline
# Так выглядят ключи и токен

Unseal Key 1: nbUCl/9XQvr/YYxrLTShQQFQ0A4AW3Wqjrbusr2x8f4u
Unseal Key 2: cSb3/rr7mYEOuxtOKQAT2q1XlMqDMNEObZ5OAgS7JpJj
Unseal Key 3: AQRtexcZ84tftbmQSax46zWWM6HifrAqhRwdUpK2jxhJ
Unseal Key 4: PCaRIwJZSnCDDBMfsSXbxkjlEY1hqreC4czLBR/SmTAZ
Unseal Key 5: +PrI5saLQiARGA1PdZxhsaCggdkK0cvUSeatb5zoK59p

Initial Root Token: hvs.FPSrL8m2FaQ4YwKpwAcYSpyI
```
3. Ввести ssh пароль от root от целевого сервера
4. Ввести access token gitlab-аккаунта с правами api (необходимо в последующем для создания токенов для gitlab-runner)
5. Далее необходимо будет создать пользователя для последующей авторизации vault

### setup ansible

1. Ввести значение для gitlab_project_slug (у вас должен быть удалённый репозиторий с этим проектом на gitlab)
2. Ввести пароль для ansible-vault (можно не запоминать)
3. Ввести ip целевого сервера

Всё готово! Теперь можно пушить свой проект на удалённый репозиторий gitlab и он автоматически будет разворачиваться на целевом сервере.

## Результаты

На целевом сервере были установлены все необходимые зависимости и развёрнут gitlab-runner с привязкой к проекту. То есть теперь ты можешь пушить свои изменения удалённый репозиторий с этим проектом на gitlab и он автоматически будет разворачиваться и проходить конвейер ci.