import json
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types
from client import MyRpcClient


class Gen(StatesGroup):
    wait_for_input = State()
    wait_for_answer = State()


class HandlerMessages:
    def __init__(
            self,
            dispatcher: Dispatcher,
            sendler: MyRpcClient
    ):
        self._dispatcher = dispatcher
        self._sendler = sendler
    def register_start_message_handler(self) -> None:
        """Начало работы с ботом, вывод клавиатуры"""
        @self._dispatcher.message_handler(commands="start")
        async def starting_bot(message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["О боте", "Сгенерировать описание"]
            keyboard.add(*buttons)
            await message.answer("Что вы хотите сделать?", reply_markup=keyboard)

    def input_message_and_wait_handler(self) -> None:
        """Пользователь выбрал пункт сгенерировать описание, перевод пользователя в состояние ожидания ввода"""
        @self._dispatcher.message_handler(Text(equals="Сгенерировать описание"))
        async def await_input_from_user(message: types.Message):
            await Gen.wait_for_input.set()
            await message.reply("Введите название фильма")

    async def get_answer_and_reply(self, id: int, message: str, state: FSMContext) -> None:
        """Получение ответа от сервера, отправка результата пользователю, сброс состояния"""
        response = await self._sendler.call(message, id)
        answer = json.loads(response.decode("UTF-8"))
        await self._dispatcher.bot.send_message(answer['user_id'], answer['text'])
        await state.finish()

    def send_and_reply_message(self) -> None:
        """Получение ответа от пользоваntля, отправка запроса к серверу"""
        @self._dispatcher.message_handler(state=Gen.wait_for_input)
        async def answer_on_input(message: types.Message, state: FSMContext):
            await message.reply("Ожидайте")
            await state.finish()
            await Gen.wait_for_answer.set()
            # запрос к серверу
            await self.get_answer_and_reply(message.from_user.id, message.text, state)

    def send_bot_about(self) -> None:
        """Вывод информации о боте"""
        @self._dispatcher.message_handler(Text(equals="О боте"))
        async def about_this_bot(message: types.Message):
            await message.reply("Бот создан для генерации описания фильмов по названию")

    def send_bot_about_state(self) -> None:
        """Вывод информации о боте"""
        @self._dispatcher.message_handler(Text(equals="О боте"), state=Gen.wait_for_answer)
        async def about_this_bot_state(message: types.Message):
            await message.reply("Бот создан для генерации описания фильмов по названию")

    def block_message_for_generation(self) -> None:
        """Блокирование пользователю новых запросов на генерацию, пока не будет получен ответ от сервера"""
        @self._dispatcher.message_handler(Text(equals="Сгенерировать описание"), state=Gen.wait_for_answer)
        async def warning_gen(message: types.Message, state: FSMContext):
            await message.reply("Дождитесь окончания генерации")
            
    def register_all_handlers(self) -> None:
        self.register_start_message_handler()
        self.input_message_and_wait_handler()
        self.send_and_reply_message()
        self.send_bot_about()
        self.send_bot_about_state()
        self.block_message_for_generation()
