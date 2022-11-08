from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.find_currency_keyboards import make_view_currency_after_find_request_keyboard, \
    view_currency_after_find_request_no_results_keyboard, make_view_currency_after_find_request_more_crypto_keyboard, \
    make_view_action_after_receiving_short_info_keyboard
from loader import dp, bot
from states.find_currency_states import FindCurrencyStates
from utils.func.view_portfolio import make_request_for_find_currency_by_slug
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.message_handler(commands="find", state="*")
@dp.message_handler(state=FindCurrencyStates.StartSearch)
async def start_search_currency_by_find(message: types.Message):
    if message.get_args() == "":
        slug = "BTC"
    elif message.get_args() is None:
        slug = message.text
    else:
        slug = message.get_args()

    data_request = await make_request_for_find_currency_by_slug(message.from_user.id, slug)

    if data_request['result'] is not None:
        await message.answer("Выберите интересующую вас криптовалюту. Можете ввести часть названия",
                             reply_markup=await make_view_currency_after_find_request_keyboard(
                                 data_request['result']['coins'],
                                 message.text.replace("/find ", "")))

        await FindCurrencyStates.FinishSearch.set()
    else:
        await message.answer("Интересующая вас криптовалюта не найдена",
                             reply_markup=view_currency_after_find_request_no_results_keyboard)

        await FindCurrencyStates.AnotherTry.set()


@dp.callback_query_handler(text="another_try", state=FindCurrencyStates.AnotherTry)
async def another_try_to_find_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Введите название интересующей вас валюты")

    await FindCurrencyStates.StartSearch.set()


@dp.callback_query_handler(text_startswith="more_crypto-", state=FindCurrencyStates.FinishSearch)
async def find_currency_for_add_cb(call: types.CallbackQuery, state: FSMContext):
    data_request = await make_request_for_find_currency_by_slug(call.from_user.id,
                                                                call.data.replace('more_crypto-', ''))

    if data_request['result'] is not None:
        await call.message.edit_text("Выберите интересующую вас криптовалюту.",
                                     reply_markup=await make_view_currency_after_find_request_more_crypto_keyboard(
                                         data_request['result']['coins']
                                     ))

        await FindCurrencyStates.FinishSearch.set()
    else:
        await call.message.edit_text("Интересующая вас криптовалюта не найдена",
                                     reply_markup=view_currency_after_find_request_no_results_keyboard)

        await FindCurrencyStates.AnotherTry.set()


@dp.callback_query_handler(state=FindCurrencyStates.FinishSearch)
async def end_search_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

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
        text = f"<code>Криптовалюта: {r.json()['result']['name']}</code>\n" \
               f"<code>Символ:       {r.json()['result']['symbol']}</code>\n" \
               f"<code>Место по рыночной капитализации: {r.json()['result']['market_cap_rank']}</code>\n\n"
        try:
            price_change_1h = r.json()['result']['market_data']['price_change_percentage_1h_in_currency']['usd']
            text += f"<code>1H  - USD: {price_change_1h}</code>\n"
        except KeyError:
            price_change_1h = None
        try:
            price_change_24h = r.json()['result']['market_data']['price_change_percentage_24h_in_currency']['usd']
            text += f"<code>24H - USD: {price_change_24h}</code>\n"
        except KeyError:
            price_change_24h = None
        try:
            price_change_7d = r.json()['result']['market_data']['price_change_percentage_7d_in_currency']['usd']
            text += f"<code>7D  - USD: {price_change_7d}</code>\n"
        except KeyError:
            price_change_7d = None
        try:
            price_change_14d = r.json()['result']['market_data']['price_change_percentage_14d_in_currency']['usd']
            text += f"<code>14D - USD: {price_change_14d}</code>\n"
        except KeyError:
            price_change_14d = None
        try:
            price_change_30d = r.json()['result']['market_data']['price_change_percentage_130_in_currency']['usd']
            text += f"<code>30D - USD: {price_change_30d}</code>\n"
        except KeyError:
            price_change_30d = None
        try:
            price_change_1y = r.json()['result']['market_data']['price_change_percentage_1y_in_currency']['usd']
            text += f"<code>1Y  - USD: {price_change_1y}</code>\n"
        except KeyError:
            price_change_1y = None

        text += f"\n" \
                f"<code>Стоимость в рублях:   {r.json()['result']['market_data']['current_price']['rub']}</code>\n" \
                f"<code>Стоимость в долларах: {r.json()['result']['market_data']['current_price']['usd']}</code>\n"

        await call.message.answer(
            text=text,
            reply_markup=await make_view_action_after_receiving_short_info_keyboard(r.json()['result']['name']))

        await FindCurrencyStates.BasicInfo.set()

        async with state.proxy() as data:
            data['observer_currency'] = call.data.lower()
            data['observer_currency_price'] = r.json()['result']['market_data']['current_price']
    else:
        # обработать
        await call.message.answer("Интересующая вас криптовалюта не найдена")
