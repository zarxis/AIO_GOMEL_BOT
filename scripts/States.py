from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    city_name = State()
    filter_name = State()
    update_Stat = State()
