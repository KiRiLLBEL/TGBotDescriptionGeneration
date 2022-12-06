# TGBotDescriptionGeneration
Проект был написан командой студентов в качестве лабораторной рабы по предмету ООП.
Данный телеграм бот генерирует описание фильма по его названию. В основе генерации лежит предобученная нейросеть RuGPTLarge3. Бот был реализован с помощью библиотеки aiogram в асинхронном режиме, все k8s манифесты хранятся в папке [manifests](/manifests).

## Структура проекта
- [Bot](#Bot)
- [Rabbitmq](#Rabbitmq)
- [Server](#Server)
- [Secrets](#Secrets)

### Bot
[bot](/bot)

- [main](/bot/app.py) - Запуск бота и подготовка диспетчера
- [client](/bot/client.py) - Класс для общения с очередьми в RabbitMQ
- [handler](/bot/handler.py) - Хендлеры для бота

### Rabbitmq
[rabbitmq](/rabbitmq) - Брокер сообщений

- [config](/rabbitmq/advanced.config) кастомизация rabbitmq

### Server
[server](/server) - Сервер, работающий в режиме потребителя и генерирующий описания

- [generate](/server/generate.py) генерация моделью текста для ответа пользователю. Используется модель ru GPT-3 Large
- [server](server/server.py) сервер

### Secrets

- Token: `kubectl create secret generic bot-auth \
    --from-literal=password='<Token>'`
- Password(Redis)  `kubectl create secret generic redis-auth \
    --from-literal=password='<password>'`

### Архитектура 
<img width="346" alt="image" src="https://user-images.githubusercontent.com/87409111/205298810-9946ecf4-efab-4c91-bf6e-36c361f6eb1c.png">

### Запуск через docker compose
Установить для бота токен и пароль для redis, в файле docker-compose
`docker-compose build -d`

### Запуск через kubernetes

Запуск всех манифестов
`kubectl apply -f "/manifests"`

