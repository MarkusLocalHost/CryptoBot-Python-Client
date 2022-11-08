from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.start_keyboard import start_keyboard
from loader import dp
from states.create_observer_states import CreateObserverStates
from states.subscribe_change_price_states import SubscribeChangePriceStates
from states.view_account_states import ViewAccountStates
from states.view_exchange_rate_states import ViewExchangeRate
from states.view_index_rating import ViewIndexRating
from states.view_portfolio_states import ViewPortfolioStates


@dp.message_handler(commands="menu", state="*")
@dp.message_handler(commands="cancel_make_observer", state="*")
async def menu_message_handler(message: types.Message, state: FSMContext):
    await message.answer("Hello", reply_markup=start_keyboard)

    await state.finish()


@dp.callback_query_handler(text="return_to_main_menu", state=ViewExchangeRate.StartChooseTypeFrom)
@dp.callback_query_handler(text="return_to_main_menu", state=ViewAccountStates.StartView)
@dp.callback_query_handler(text="return_to_main_menu", state=ViewPortfolioStates.StartView)
@dp.callback_query_handler(text="return_to_main_menu", state=ViewPortfolioStates.AddCurrency)
@dp.callback_query_handler(text="return_to_main_menu", state=CreateObserverStates.StartCreate)
@dp.callback_query_handler(text="return_to_main_menu", state=CreateObserverStates.StartChooseTypeOfView)
@dp.callback_query_handler(text="return_to_main_menu", state=SubscribeChangePriceStates.StartSubscribe)
@dp.callback_query_handler(text="return_to_main_menu", state=ViewIndexRating.StartChooseType)
@dp.callback_query_handler(text="return_to_main_menu", state=ViewExchangeRate.MakeRequest)
@dp.callback_query_handler(text="return_to_main_menu")
async def menu_return(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text("Hello", reply_markup=start_keyboard)

    await state.finish()


@dp.callback_query_handler(text="cancel_make_observer", state=CreateObserverStates.FinishSearchCurrency)
@dp.callback_query_handler(text="cancel_make_observer", state=CreateObserverStates.ViewDataForObserver)
async def menu_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text("Hello", reply_markup=start_keyboard)

    await state.finish()
