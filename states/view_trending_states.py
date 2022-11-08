from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewTrendingStates(StatesGroup):
    StartView = State()
    SendNameOfTrendingCurrency = State()
    SendBasicInfoOfTrendingCurrency = State()
