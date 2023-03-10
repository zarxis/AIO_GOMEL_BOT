import logging
import sqlite3

from scripts import sql
from scripts import weather_py

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN

storage = MemoryStorage()
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


class StateMachine(StatesGroup):
    city_name = State()
    filter_name = State()


def KeyB() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/weather'),
           KeyboardButton('/to_filter'))
    return kb


@dp.message_handler(commands=['start'])
async def is_start(message: types.Message):
    await message.answer('Привет! '
                         'этот бот может подсказать тебе погоду! ',
                         #'или посчитать как часто ты материшься в чатах:)',
                         reply_markup=KeyB())

    async def get_user(message: types.Message):
        try:
            u_reg = message.from_user.id
            u_fname = message.from_user.username
            u_lname = message.from_user.last_name
            u_stat = 0
            sql.db_CON_BadWord.INSERT(user_id=u_reg, first_name=u_fname, last_name=u_lname, stat=u_stat)
            await message.answer('Поздравляю, теперь ты зарегестрирован :)')
        except:
            await message.answer(message)

    await get_user(message)


# --------------------Погода--------------------------------
@dp.message_handler(commands=['weather'])
async def is_start(message: types.Message):
    await message.answer('Введите название города')
    await StateMachine.city_name.set()


@dp.message_handler(state=StateMachine.city_name)
async def get_city_name(message: types.Message, state: FSMContext):
    await state.update_data(c_name=message.text)
    # если остановить просто message можно увидеть подробную информацию о сообщение!
    data = await state.get_data()
    await message.answer(f"Название города: {data['c_name']}")
    await state.finish()
    await weather_py.GetWeather(message)
# ----------------------------------------------------------


# --------------------Фильтр--------------------------------
@dp.message_handler(commands='to_filter')
async def add_to_db(message: types.Message):
    await message.answer('Видимо вы хотите добавить одно из плохих слов.')
    await StateMachine.filter_name.set()


@dp.message_handler(state=StateMachine.filter_name)
async def to_db(message: types.Message, state: FSMContext):
    await state.update_data(f_name=message.text)
    Fdata = await state.get_data()
    await state.finish()
    try:
        sql.db_CON_WORD.INSERT(message.text)
        await message.answer("Слово добавлено!")
    except:
        if sqlite3.Error:
            await message.answer('Упс, что-то не так...')
            await message.answer(sqlite3.Error)
# ----------------------------------------------------------


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
