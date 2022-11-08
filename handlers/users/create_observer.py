import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.create_observer_keyboards import view_actions_in_create_price_observer, \
    make_view_actions_in_search_currency_for_observer_keyboard, make_view_currency_after_find_request_keyboard, \
    view_action_after_receiving_short_info, make_view_supported_vs_currencies_after_receiving_keyboard, \
    view_action_after_receiving_observer_info, view_actions_after_create_price_observer
from loader import dp, bot
from states.create_observer_states import CreateObserverStates
from states.find_currency_states import FindCurrencyStates
from states.view_account_states import ViewAccountStates
from states.view_trending_states import ViewTrendingStates
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.message_handler(commands="new_observer", state="*")
@dp.message_handler(text="Создать обсервер", state="*")
async def create_new_observer(message: types.Message):
    await message.answer("Введите название криптовалюты на английском языке.\n"
                         "К примеру: bitcoin\n"
                         "P.S. работает пока только по имени",
                         reply_markup=view_actions_in_create_price_observer)

    await CreateObserverStates.StartCreate.set()


@dp.callback_query_handler(text="create_observer", state=ViewAccountStates.ViewObservers)
@dp.callback_query_handler(text="create_price_observer_from_start_menu")
async def create_new_observer_cb(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите название криптовалюты на английском языке.\n"
                                 "К примеру: bitcoin\n"
                                 "P.S. работает пока только по имени",
                                 reply_markup=view_actions_in_create_price_observer)

    await CreateObserverStates.StartCreate.set()


@dp.message_handler(state=CreateObserverStates.StartCreate)
async def start_search_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["search_text"] = message.text

    await message.answer(text="Выберите вариант просмотра",
                         reply_markup=await make_view_actions_in_search_currency_for_observer_keyboard(message.text))

    await CreateObserverStates.StartChooseTypeOfView.set()


@dp.callback_query_handler(text="view_currency_standard_view", state=CreateObserverStates.StartChooseTypeOfView)
async def view_search_currencies_in_standard_view(call: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "currency_name": data_state["search_text"],
        "currency_slug": ""
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/search/try_find_currency"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text("Выберите интересующую вас криптовалюту. Можете ввести часть названия",
                                     reply_markup=await make_view_currency_after_find_request_keyboard(
                                         r.json()['result']["coins"]))

        await CreateObserverStates.StartSearchCurrency.set()
    else:
        # обработать
        await call.message.edit_text("Интересующая вас криптовалюта не найдена")


@dp.callback_query_handler(text="cancel_make_observer", state=CreateObserverStates.FinishSearchCurrency)
@dp.callback_query_handler(text="cancel_make_observer", state=CreateObserverStates.FinishSetSupportedCurrency)
@dp.callback_query_handler(text="cancel_make_observer", state=CreateObserverStates.ViewDataForObserver)
async def cancel_create_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()


@dp.callback_query_handler(state=CreateObserverStates.StartSearchCurrency)
async def end_search_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    data = {
        "telegramUserID": call.from_user.id,
        "currency_slug": call.data.lower()
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
            reply_markup=view_action_after_receiving_short_info)

        await CreateObserverStates.FinishSearchCurrency.set()

        async with state.proxy() as data:
            data['observer_currency'] = call.data.lower()
            data['observer_currency_price'] = r.json()['result']['market_data']['current_price']
    else:
        # обработать
        await call.message.answer("Интересующая вас криптовалюта не найдена")


# выбор валюты в которой отслеживать
@dp.callback_query_handler(text="make_observer", state=ViewTrendingStates.SendBasicInfoOfTrendingCurrency)
@dp.callback_query_handler(text="make_observer", state=CreateObserverStates.FinishSearchCurrency)
@dp.callback_query_handler(text="make_observer", state=FindCurrencyStates.BasicInfo)
async def start_set_supported_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data = {
        "telegramUserID": call.from_user.id,
    }
    endpoint = f"http://127.0.0.1:8080/api/info/supported_vs_currencies/view"
    token = await generate_token(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text(text="Выберите валюту в которой отслеживать цену",
                                     reply_markup=await make_view_supported_vs_currencies_after_receiving_keyboard(
                                         r.json()['result']))

        await CreateObserverStates.FinishSetSupportedCurrency.set()
    else:
        # обработать
        await call.message.answer("Интересующая вас криптовалюта не найдена")


# выбор значения для оповещения
@dp.callback_query_handler(state=CreateObserverStates.FinishSetSupportedCurrency)
async def start_set_value_supported_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['observer_supported_vs_currency'] = call.data.lower()

    await call.message.edit_text(
        f"Введите значение на котором вас оповестить в валюте {call.data} или изменение в процентах со знаком процента,"
        f" к примеру +10% или -15%\n\n"
        f"<code>"
        f"Цена сейчас в выбранной валюте {data['observer_currency_price'][call.data]}"
        f"</code>")

    await CreateObserverStates.FinishSetExpectedValue.set()


# просмотр данных для обсервера
@dp.message_handler(state=CreateObserverStates.FinishSetExpectedValue)
async def view_data_for_create_observer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "%" in message.text:
            value = message.text.replace("%", "")
            if "-" in value:
                value = value.replace("-", "")
                positive = False
            elif "+" in value:
                value = value.replace("+", "")
                positive = True
            else:
                positive = True

            try:
                if positive:
                    data['observer_value_for_supported_vs_currency'] = float(
                        data['observer_currency_price'][data['observer_supported_vs_currency']]) + float(
                        data['observer_currency_price'][data['observer_supported_vs_currency']]) * float(
                        value) / 100
                else:
                    data['observer_value_for_supported_vs_currency'] = float(
                        data['observer_currency_price'][data['observer_supported_vs_currency']]) - float(
                        data['observer_currency_price'][data['observer_supported_vs_currency']]) * float(
                        value) / 100
            except ValueError:
                await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

                await CreateObserverStates.FinishSetExpectedValue.set()

                return
        else:
            try:
                data['observer_value_for_supported_vs_currency'] = float(message.text)
            except ValueError:
                await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

                await CreateObserverStates.FinishSetExpectedValue.set()

                return

    data_state = await state.get_data()

    await message.answer(f"Просмотр данных для создания наблюдателя\n\n"
                         f"<code>"
                         f"Выбранная валюта {data_state['observer_currency']}\n"
                         f"Отслеживание в валюте {data_state['observer_supported_vs_currency']}\n"
                         f"Значение для отслеживания {data_state['observer_value_for_supported_vs_currency']}"
                         f"</code>",
                         reply_markup=view_action_after_receiving_observer_info)

    await CreateObserverStates.ViewDataForObserver.set()


# выбор значения для оповещения
@dp.callback_query_handler(text="finish_make_observer", state=CreateObserverStates.ViewDataForObserver)
async def start_set_value_supported_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    if float(data_state['observer_currency_price'][data_state['observer_supported_vs_currency']]) > float(
            data_state['observer_value_for_supported_vs_currency']):
        is_up_direction = False
    else:
        is_up_direction = True

    data = {
        "telegramUserID": call.from_user.id,
        "cryptoID": data_state['observer_currency'],
        "currencyOfValue": data_state['observer_supported_vs_currency'],
        "expectedValue": float(data_state['observer_value_for_supported_vs_currency']),
        "isUpDirection": is_up_direction
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/observers/price_observer/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] == "observer started":
        await call.message.edit_text(f"Обсервер успешно создан и запущен",
                                     reply_markup=view_actions_after_create_price_observer)

        await state.finish()

    elif r.json()['result'] == "observer created":
        await call.message.edit_text(f"Обсервер успешно создан но не запущен из-за лимитов",
                                     reply_markup=view_actions_after_create_price_observer)

        await state.finish()

    else:
        await call.message.edit_text(f"Произошла ошибка",
                                     reply_markup=view_actions_after_create_price_observer)

        await state.finish()
