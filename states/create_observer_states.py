from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateObserverStates(StatesGroup):
    StartCreate = State()
    StartChooseTypeOfView = State()
    StartSearchCurrency = State()
    FinishSearchCurrency = State()
    FinishSetSupportedCurrency = State()
    FinishSetExpectedValue = State()
    ViewDataForObserver = State()
