from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStates(StatesGroup):
    SelectLanguage = State()
    FinishCreateAccount = State()
