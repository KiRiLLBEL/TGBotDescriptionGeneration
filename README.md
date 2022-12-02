# TGBotDescriptionGeneration
Бот генерирующий описание фильма по его названию

## Bot
[bot](/bot)

- [main](/bot/app.py)
- [client](/bot/client.py)
- [handler](/bot/handler.py)

## Rabbitmq
[rabbitmq](/rabbitmq)

Очередь сообщений
- [config](/rabbitmq/advanced.config) кастомизация rabbitmq

## Server
[server](/server)

- [generate](/server/generate.py) генерация моделью текста для ответа пользователю. Используется модель ru GPT-3 Large
- [server](server/server.py) сервер

## Архитектура 
<img width="346" alt="image" src="https://user-images.githubusercontent.com/87409111/205298810-9946ecf4-efab-4c91-bf6e-36c361f6eb1c.png">
