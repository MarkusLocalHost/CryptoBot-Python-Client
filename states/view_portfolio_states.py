from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewPortfolioStates(StatesGroup):
    StartView = State()
    StartViewCurrency = State()

    AddCurrency = State()
    FindCurrency = State()
    FinishFindCurrency = State()
    Type = State()
    CountOfCurrency = State()
    PriceOfCurrency = State()
    ViewFinalData = State()

    StartViewRecord = State()
    StartChangeCountRecord = State()
    StartChangePriceRecord = State()
    StartDeleteRecord = State()
