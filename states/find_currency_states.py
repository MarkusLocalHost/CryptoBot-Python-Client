from aiogram.dispatcher.filters.state import StatesGroup, State


class FindCurrencyStates(StatesGroup):
    StartSearch = State()
    FinishSearch = State()
    AnotherTry = State()
    BasicInfo = State()
