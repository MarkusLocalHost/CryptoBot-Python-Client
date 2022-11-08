from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewAccountStates(StatesGroup):
    StartView = State()

    ViewObservers = State()
    ViewCurrentObserver = State()
    DeleteCurrentObserver = State()
    ChangeStatusCurrentObserver = State()

    ViewPercentageObserver = State()
    ViewCurrentPercentageObserver = State()
    DeleteCurrentPercentageObserver = State()

    ViewAccountSubscription = State()
    EnterPromoCode = State()
    IncorrectPromoCode = State()
