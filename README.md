# TGBotDescriptionGeneration
Бот генерирующий описание фильма по его названию

## [bot](/bot)
Для генерации используется модель ru GPT-3 Large
- [main](/bot/app.py)
- [client](/bot/client.py)
- [handler](/bot/handler.py)

## [rabbitmq](/rabbitmq)
Очередь сообщений
- [config](/rabbitmq/advanced.config) кастомизация rabbitmq

## [server](/server)
- [generate](/server/generate.py) генерация текста моделью для ответа пользователю
- [server](server/server.py) сервер
