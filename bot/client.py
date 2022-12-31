import uuid
import asyncio
import json
import os
import logging
from typing import MutableMapping
from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue,
)

class MyRpcClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self) -> None:
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = asyncio.get_running_loop()

    async def connect(self) -> "MyRpcClient":
        """Установка соединения с RabbitMQ, создание очереди для получения запросов. Начать слушать очередь"""
        self.connection = await connect(
            os.environ["AMQP_URL"], loop=self.loop,
        )
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)
        return self

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        """Callback. Действие на возврат ответа message от сервера"""
        if message.correlation_id is None:
            logging.warning(f" [x] Bad message {message!r}")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)
        inputJson = message.body.decode("UTF-8")
        inputMessage = json.loads(inputJson)
        logging.info(" [x] Message from server: %r", inputMessage['text'])
        logging.info(" [x] Response complete")

    async def call(self, text: str, id: int) -> int:
        """Создать запрос к очереди. Передать id пользователя и его сообщение - text в формате json"""
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        logging.info(" [x] Message from user: %r", text)
        params = {
            "user_id": id,
            "text": text
        }
        jsonParams = json.dumps(params)
        self.futures[correlation_id] = future

        try:
            await self.channel.default_exchange.publish(
                Message(
                    jsonParams.encode(),
                    content_type="application/json",
                    correlation_id=correlation_id,
                    reply_to=self.callback_queue.name,
                ),
                routing_key="rpc_queue",
            )
        except:
            logging.exception(" [x] Message not sending")

        return await future