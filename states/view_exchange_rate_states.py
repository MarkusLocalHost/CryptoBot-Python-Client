from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewExchangeRate(StatesGroup):
    StartChooseTypeFrom = State()
    StartChooseBank = State()
    StartChooseWallet = State()
    StartChooseCrypto = State()

    StartChooseTypeTo = State()
    FinishChooseBank = State()
    FinishChooseWallet = State()
    FinishChooseCrypto = State()

    SetTypeOfCurrencyOfExchange = State()
    SetValueOfExchange = State()

    MakeRequest = State()

    ViewAllVariants = State()
    ViewCurrentVariants = State()

