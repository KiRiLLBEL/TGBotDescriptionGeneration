from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
import pika
import codecs
import asyncio
import aio_pika
import os
amqp_url = os.environ['AMQP_URL']
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

conn_params = pika.URLParameters(amqp_url)

async def send(id, text) -> None:
    await bot.send_message(id, text)

def callback(ch, method, properties, body):
    input = codecs.decode(body, 'UTF-8')
    id, text = input.split("&")
    print(text)
    asyncio.run(send(id, text))



class Gen(StatesGroup):
    wait_for_input = State()
    wait_for_answer = State()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["О боте", "Сгенерировать описание"]
    keyboard.add(*buttons)
    await message.answer("Что вы хотите сделать?", reply_markup=keyboard)

@dp.message_handler(Text(equals="О боте"))
async def with_puree(message: types.Message):
    await message.reply("Бот создан для генерации описания фильмов, по названию")

@dp.message_handler(Text(equals="Сгенерировать описание"))
async def with_pure(message: types.Message):
    await Gen.wait_for_input.set()
    await message.reply("Введите название фильма")

@dp.message_handler(state=Gen.wait_for_input)
async def process_name(message: types.Message, state: FSMContext):
    output = str(message.from_user.id) + "&" + message.text
    # connection = await aio_pika.connect_robust(
    #     amqp_url,
    # )

    # async with connection:
    #     channel = await connection.channel()

    #     await channel.default_exchange.publish(
    #         aio_pika.Message(body=output.encode()),
    #         routing_key='first-queue',
    #     )
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue="first-queue")
    channel.basic_publish(exchange='', routing_key='first-queue', body=output)
    connection.close()
    await message.reply("Ожидайте")
    await state.finish()
    await Gen.wait_for_answer.set()

@dp.message_handler(state=Gen.wait_for_answer)
async def warning_gen(message: types.Message, state: FSMContext):
    await message.reply("Дождитесь окончания генерации")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Бот создан для генерации описания фильмов, по названию")

async def main() -> None:
    connection2 = await aio_pika.connect_robust(
        amqp_url, 
    )

    queue_name = "second-queue"

    async with connection2:
        channel = await connection2.channel()

        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    input = codecs.decode(message.body, 'UTF-8')
                    id, text = input.split("&")
                    await bot.send_message(id, text)
                    new_state = FSMContext(storage, id, id)
                    await new_state.finish()
                    if queue.name in message.body.decode():
                        break


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp)
    