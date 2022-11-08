from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewIndexRating(StatesGroup):
    StartChooseType = State()

    StartView = State()
