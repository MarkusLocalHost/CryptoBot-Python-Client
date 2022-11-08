from aiogram.dispatcher.filters.state import StatesGroup, State


class SubscribeChangePriceStates(StatesGroup):
    StartSubscribe = State()
    Settings = State()
    FilterSettings = State()
    ReceiveXForFilter = State()
    SecondFilterSettings = State()
    ReceiveSecondXForFilter = State()
    ViewInfo = State()
