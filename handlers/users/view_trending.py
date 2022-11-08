from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.view_trending_keyboards import view_source_for_trending_currencies_keyboard, \
    make_view_action_after_receiving_short_info_keyboard
from loader import dp, bot
from states.view_trending_states import ViewTrendingStates
from utils.func.view_trending import make_message_by_data_request
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.message_handler(commands="view_trending", state="*")
@dp.message_handler(text="Просмотр Trending Cryptocurrency", state="*")
async def view_source_for_trending_currency(message: types.Message):
    await message.answer("Выберите источник для просмотра популярных на данных момент криптовалют.",
                         reply_markup=view_source_for_trending_currencies_keyboard)

    await ViewTrendingStates.StartView.set()


@dp.callback_query_handler(text="back", state=ViewTrendingStates.SendNameOfTrendingCurrency)
async def view_source_for_trending_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text("Выберите источник для просмотра популярных на данных момент криптовалют.",
                                 reply_markup=view_source_for_trending_currencies_keyboard)

    await ViewTrendingStates.StartView.set()


@dp.callback_query_handler(text="close_trending", state=ViewTrendingStates.StartView)
async def close_trending_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await state.finish()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="back", state=ViewTrendingStates.SendBasicInfoOfTrendingCurrency)
@dp.callback_query_handler(state=ViewTrendingStates.StartView)
async def end_search_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    if call.data != 'back':
        async with state.proxy() as data:
            data['current_trending_currency_source'] = call.data.lower()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id
    }

    if call.data == "coingecko_trending" or \
            data_state['current_trending_currency_source'] == 'coingecko_trending' and call.data == 'back':
        data["source"] = "coingecko_trending"
    elif call.data == "coinmarketcap_trending" or \
            data_state['current_trending_currency_source'] == 'coinmarketcap_trending' and call.data == 'back':
        data["source"] = "coinmarketcap_trending"
    elif call.data == "coinmarketcap_gainers" or \
            data_state['current_trending_currency_source'] == 'coinmarketcap_gainers' and call.data == 'back':
        data["source"] = "coinmarketcap_gainers"
    elif call.data == "coinmarketcap_losers" or \
            data_state['current_trending_currency_source'] == 'coinmarketcap_losers' and call.data == 'back':
        data["source"] = "coinmarketcap_losers"
    elif call.data == "coinmarketcap_most_visited" or \
            data_state['current_trending_currency_source'] == 'coinmarketcap_most_visited' and call.data == 'back':
        data["source"] = "coinmarketcap_most_visited"
    elif call.data == "coinmarketcap_recently_added" or \
            data_state['current_trending_currency_source'] == 'coinmarketcap_recently_added' and call.data == 'back':
        data["source"] = "coinmarketcap_recently_added"
    else:
        await call.message.edit_text(text="Непридвиденная ошибка")

    token = await generate_token(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    endpoint = f"http://127.0.0.1:8080/api/info/trending"

    r = await make_request_get(endpoint, headers)

    await make_message_by_data_request(r, call)


@dp.callback_query_handler(state=ViewTrendingStates.SendNameOfTrendingCurrency)
async def view_basic_info_for_trending_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data = {
        "telegramUserID": call.from_user.id,
        "currencyID": call.data
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/info/currency/data/short_version"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text(f"Криптовалюта: {r.json()['result']['name']}\n"
                                     f"Символ: {r.json()['result']['symbol']}\n"
                                     f"Место по рыночной капитализации: {r.json()['result']['market_cap_rank']}\n"
                                     f"\n"
                                     f"Стоимость в рублях:   {r.json()['result']['market_data']['current_price']['rub']}\n"
                                     f"Стоимость в долларах: {r.json()['result']['market_data']['current_price']['usd']}\n",
                                     reply_markup=await make_view_action_after_receiving_short_info_keyboard(
                                         call.data.lower()))

        # для обсервера
        async with state.proxy() as data:
            data['observer_currency'] = call.data.lower()
            data['observer_currency_price'] = r.json()['result']['market_data']['current_price']

        await ViewTrendingStates.SendBasicInfoOfTrendingCurrency.set()
    else:
        # обработать
        await call.message.edit_text("Интересующая вас криптовалюта не найдена")
