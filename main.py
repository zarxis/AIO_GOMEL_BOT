import logging

import mysql
from mysql import connector

from scripts import KeyBoard
from scripts import TEST_SQL
from scripts import weather_py
from scripts import States

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext

from config import TOKEN

storage = MemoryStorage()
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def is_start(message: types.Message):
    await message.answer('Привет! '
                         'этот бот может подсказать тебе погоду! ',
                         # 'или посчитать как часто ты материшься в чатах:)',
                         reply_markup=KeyBoard.KeyB())

    async def get_user(message: types.Message):
        try:
            u_reg = message.from_user.id
            u_fname = message.from_user.username
            u_lname = message.from_user.last_name
            u_stat = 0
            TEST_SQL.db_CON_BadWord.INSERT(
                user_id=u_reg,
                first_name=u_fname,
                last_name=u_lname,
                stat=u_stat)
        except mysql.connector.errors.IntegrityError:
            await message.answer("Кажется вы уже зарегистрированы!")
        except mysql.connector.Error:
            await message.answer("Пожалуйста, перешлите следующие сообщение мне! @Glen_Lex ")

    await get_user(message)


# --------------------Погода--------------------------------
@dp.message_handler(commands=['weather'])
async def is_start(message: types.Message):
    await message.answer('Введите название города')
    await States.StateMachine.city_name.set()


@dp.message_handler(state=States.StateMachine.city_name)
async def get_city_name(message: types.Message, state: FSMContext):
    await state.update_data(c_name=message.text)  # если остановить просто
    # message можно увидеть подробную информацию о сообщение!
    await state.finish()
    """
    while 1:
        await weather_py.GetWeather(message)
        time.sleep(0.3)
    """
    await weather_py.GetWeather(message)


# ----------------------------------------------------------


# --------------------Фильтр--------------------------------
@dp.message_handler(commands='to_filter')
async def add_to_db(message: types.Message):
    await message.answer('Видимо вы хотите добавить одно из плохих слов. \n Введите его:)')
    await States.StateMachine.filter_name.set()


@dp.message_handler(state=States.StateMachine.filter_name)
async def to_db(message: types.Message, state: FSMContext):
    await state.update_data(f_name=message.text)
    # Fdata = await state.get_data()
    TEST_SQL.db_CON_WORD.INSERT(message.text)
    await message.answer("Слово добавлено!")
    await state.finish()


# ----------------------------------------------------------


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
