import os
import asyncio
import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import Redis
import redis

from client import MyRpcClient
from handler import HandlerMessages

logging.basicConfig(level=logging.INFO)

async def prepare(sendler: MyRpcClient) -> Dispatcher:
    """Создание и конфигурация бота, подключение к RabbitMQ"""
    storage = RedisStorage2(host=os.environ['REDIS_HOST'], db=5, port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'])
    bot = Bot(os.environ['TOKEN'])
    dp = Dispatcher(bot, storage=storage)
    handler = HandlerMessages(dp, sendler)
    handler.register_all_handlers()
    return dp

async def main() -> None:
    # Установка соединения с RabbitMQ
    sendler = await MyRpcClient().connect()
    # Создание dispatcher
    dp = await prepare(sendler)
    # Запуск бота
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

