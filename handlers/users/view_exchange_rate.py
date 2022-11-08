from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from keyboards.inline.view_exchange_rate_keyboards import view_type_exchange_type, view_banks, view_cryptos, \
    view_wallets, make_view_banks_keyboard, make_view_wallets_keyboard, view_type_exchange_type_only_crypto, \
    view_type_exchange_type_only_bank_and_wallet
from loader import dp, bot
from states.view_exchange_rate_states import ViewExchangeRate
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.callback_query_handler(text="back", state=ViewExchangeRate.StartChooseBank)
@dp.callback_query_handler(text="back", state=ViewExchangeRate.StartChooseWallet)
@dp.callback_query_handler(text="back", state=ViewExchangeRate.StartChooseCrypto)
@dp.callback_query_handler(text="again", state=ViewExchangeRate.MakeRequest)
@dp.callback_query_handler(text="view_exchange_rate_from_bestchange_from_start_menu", state="*")
async def start_choose_exchange_rate_from_bestchange_cb(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Выберите что отдаете", reply_markup=view_type_exchange_type)

    if call.data == "again":
        await state.finish()

    await ViewExchangeRate.StartChooseTypeFrom.set()


# выбор банка
@dp.callback_query_handler(text="view_banks", state=ViewExchangeRate.StartChooseTypeFrom)
@dp.callback_query_handler(text="view_banks", state=ViewExchangeRate.StartChooseTypeTo)
async def choose_bank_to_exchange(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Выберите банк", reply_markup=view_banks)

    if await state.get_state() == "ViewExchangeRate:StartChooseTypeFrom":
        await ViewExchangeRate.StartChooseBank.set()
    elif await state.get_state() == "ViewExchangeRate:StartChooseTypeTo":
        await ViewExchangeRate.FinishChooseBank.set()


# выбор кошелька
@dp.callback_query_handler(text="view_wallets", state=ViewExchangeRate.StartChooseTypeFrom)
@dp.callback_query_handler(text="view_wallets", state=ViewExchangeRate.StartChooseTypeTo)
async def choose_wallet_to_exchange(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Выберите эл.кошелек", reply_markup=view_wallets)

    if await state.get_state() == "ViewExchangeRate:StartChooseTypeFrom":
        await ViewExchangeRate.StartChooseWallet.set()
    elif await state.get_state() == "ViewExchangeRate:StartChooseTypeTo":
        await ViewExchangeRate.FinishChooseWallet.set()


# выбор крипты
@dp.callback_query_handler(text="view_cryptos", state=ViewExchangeRate.StartChooseTypeFrom)
@dp.callback_query_handler(text="view_cryptos", state=ViewExchangeRate.StartChooseTypeTo)
async def choose_crypto_to_exchange(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Выберите криптовалюту", reply_markup=view_cryptos)

    if await state.get_state() == "ViewExchangeRate:StartChooseTypeFrom":
        await ViewExchangeRate.StartChooseCrypto.set()
    elif await state.get_state() == "ViewExchangeRate:StartChooseTypeTo":
        await ViewExchangeRate.FinishChooseCrypto.set()


# выбор на что менять
@dp.callback_query_handler(text="confirm", state=ViewExchangeRate.StartChooseBank)
@dp.callback_query_handler(text="confirm", state=ViewExchangeRate.StartChooseWallet)
@dp.callback_query_handler(state=ViewExchangeRate.StartChooseCrypto)
async def start_choose_exchange_rate_to_bestchange_cb(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    if await state.get_state() == "ViewExchangeRate:StartChooseBank":
        async with state.proxy() as data:
            data["from"] = "bank"
    if await state.get_state() == "ViewExchangeRate:StartChooseWallet":
        async with state.proxy() as data:
            data["from"] = "wallet"
    elif await state.get_state() == "ViewExchangeRate:StartChooseCrypto":
        async with state.proxy() as data:
            data["from"] = "crypto"
            data["from_crypto"] = call.data

    if data["from"] == "bank" or data["from"] == "wallet":
        await call.message.edit_text(text="Выберите что получаете", reply_markup=view_type_exchange_type_only_crypto)
    else:
        await call.message.edit_text(text="Выберите что получаете",
                                     reply_markup=view_type_exchange_type_only_bank_and_wallet)

    await ViewExchangeRate.StartChooseTypeTo.set()


# определяем валюту для лимита
@dp.callback_query_handler(text="confirm", state=ViewExchangeRate.FinishChooseBank)
@dp.callback_query_handler(text="confirm", state=ViewExchangeRate.FinishChooseWallet)
@dp.callback_query_handler(state=ViewExchangeRate.FinishChooseCrypto)
async def choose_currency_cb(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    if await state.get_state() == "ViewExchangeRate:FinishChooseBank":
        async with state.proxy() as data:
            data["to"] = "bank"
    if await state.get_state() == "ViewExchangeRate:FinishChooseWallet":
        async with state.proxy() as data:
            data["to"] = "wallet"
    elif await state.get_state() == "ViewExchangeRate:FinishChooseCrypto":
        async with state.proxy() as data:
            data["to"] = "crypto"
            data["to_crypto"] = call.data

    view_currency_for_set_limit_of_exchange = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_currency_for_set_limit_of_exchange.add(types.InlineKeyboardButton(
        text="В рублях",
        callback_data="rub"))
    view_currency_for_set_limit_of_exchange.add(types.InlineKeyboardButton(
        text="В криптовалюте",
        callback_data="crypto"))

    await call.message.edit_text(
        text="Выберите необходимую валюту в которой будет определяться нужное значение для обмена",
        reply_markup=view_currency_for_set_limit_of_exchange)

    await ViewExchangeRate.SetTypeOfCurrencyOfExchange.set()


# определяем количество валюты для лимита
@dp.callback_query_handler(state=ViewExchangeRate.SetTypeOfCurrencyOfExchange)
async def choose_value_cb(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data["currency_of_limit_to_exchange"] = call.data

    await call.message.edit_text(text="Введите количество")

    await ViewExchangeRate.SetValueOfExchange.set()


# выбор нескольких банков с которых менять
@dp.callback_query_handler(state=ViewExchangeRate.StartChooseBank)
@dp.callback_query_handler(state=ViewExchangeRate.FinishChooseBank)
async def multiple_choose_banks(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    direction = ""
    if await state.get_state() == "ViewExchangeRate:StartChooseBank":
        direction = "from_banks"
    elif await state.get_state() == "ViewExchangeRate:FinishChooseBank":
        direction = "to_banks"

    async with state.proxy() as data:
        try:
            data_banks = data[direction]
        except KeyError:
            data_banks = ""
        if call.data in data_banks:
            data[direction] = data_banks.replace(call.data, "")
        else:
            data[direction] = data_banks + call.data

    await call.message.edit_text(text="Выберите один или несколько банков",
                                 reply_markup=await make_view_banks_keyboard(data[direction]))


# выбор нескольких кошельков с которых менять
@dp.callback_query_handler(state=ViewExchangeRate.StartChooseWallet)
@dp.callback_query_handler(state=ViewExchangeRate.FinishChooseWallet)
async def multiple_choose_wallets(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    direction = ""
    if await state.get_state() == "ViewExchangeRate:StartChooseWallet":
        direction = "from_wallets"
    elif await state.get_state() == "ViewExchangeRate:FinishChooseWallet":
        direction = "to_wallets"

    async with state.proxy() as data:
        try:
            data_wallets = data[direction]
        except KeyError:
            data_wallets = ""
        if call.data in data_wallets:
            data[direction] = data_wallets.replace(call.data, "")
        else:
            data[direction] = data_wallets + call.data

    await call.message.edit_text(text="Выберите один или несколько эл.кошельков",
                                 reply_markup=await make_view_wallets_keyboard(data[direction]))


# делаем запрос
@dp.message_handler(state=ViewExchangeRate.SetValueOfExchange)
async def make_request(message: types.Message, state: FSMContext):
    try:
        limit_value = float(message.text)

        if limit_value > 0:
            wait_message = await message.answer("Идет обработка")

            data_state = await state.get_data()

            data = {
                "telegramUserID": message.from_user.id,
                "limitCurrency": data_state["currency_of_limit_to_exchange"],
                "limitValue": message.text
            }

            if data_state["from"] == "bank":
                data["exchangeFrom"] = data_state["from_banks"]
                data["exchangeFromType"] = "bank"
            elif data_state["from"] == "wallet":
                data["exchangeFrom"] = data_state["from_wallets"]
                data["exchangeFromType"] = "wallet"
            elif data_state["from"] == "crypto":
                data["exchangeFrom"] = data_state["from_crypto"]
                data["exchangeFromType"] = "crypto"

            if data_state["to"] == "bank":
                data["exchangeTo"] = data_state["to_banks"]
                data["exchangeToType"] = "bank"
            elif data_state["to"] == "wallet":
                data["exchangeTo"] = data_state["to_wallets"]
                data["exchangeToType"] = "wallet"
            elif data_state["to"] == "crypto":
                data["exchangeTo"] = data_state["to_crypto"]
                data["exchangeToType"] = "crypto"

            token = await generate_token(data)
            endpoint = f"http://127.0.0.1:8080/api/info/exchange/bestchange"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            r = await make_request_get(endpoint, headers)

            view_actions_for_variants = types.InlineKeyboardMarkup(resize_keyboard=True)
            if r.json()['result'] != {}:
                text = ""
                view_actions_for_variants.add(types.InlineKeyboardButton(
                    text="Посмотреть все варинаты",
                    callback_data="view_all_variants"))

                async with state.proxy() as data_state:
                    data_state["data_exchange_variants"] = r.json()['result']

                response_data = r.json()['result']
                for key in response_data.keys():
                    num = 0
                    text += f"{key}\n\n"
                    for variant in r.json()["result"][key]:
                        if num == 3:
                            break
                        else:
                            num += 1

                        text += f"Обменник {variant['Exchanger']}\n" \
                                f"Курс {variant['Rate']}\n" \
                                f"Рейтинг {variant['GoodReviews']}😀  {variant['BadReviews']}😡\n" \
                                f"{hlink('Ссылка', variant['Link'])}\n\n"

                    view_actions_for_variants.add(types.InlineKeyboardButton(
                        text=f"Просмотреть только для {key}",
                        callback_data=f"{key}"))
            else:
                text = "Варианты не найдены"

                view_actions_for_variants.add(types.InlineKeyboardButton(
                    text="Начать заново",
                    callback_data="again"))

            view_actions_for_variants.add(types.InlineKeyboardButton(
                text="Вернуться в главное меню",
                callback_data="return_to_main_menu"))

            await ViewExchangeRate.MakeRequest.set()

            await bot.edit_message_text(text, message.chat.id, wait_message.message_id, reply_markup=view_actions_for_variants)

        else:
            await message.answer(text="Введеное число меньше нуля, попробуйте еще раз")

    except ValueError:
        await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")


# возвращение
@dp.callback_query_handler(text="back", state=ViewExchangeRate.ViewAllVariants)
@dp.callback_query_handler(text="back", state=ViewExchangeRate.ViewCurrentVariants)
async def back_to_view_start_page_for_exchange_variants(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()
    response_data = data_state["data_exchange_variants"]

    text = ""
    view_actions_for_variants = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_actions_for_variants.add(types.InlineKeyboardButton(
        text="Посмотреть все варинаты",
        callback_data="view_all_variants"))
    for key in response_data.keys():
        num = 0
        text += f"{key}\n\n"
        for variant in response_data[key]:
            if num == 3:
                break
            else:
                num += 1

            text += f"Обменник {variant['Exchanger']}\n" \
                    f"Курс {variant['Rate']}\n" \
                    f"Рейтинг {variant['GoodReviews']}😀  {variant['BadReviews']}😡\n" \
                    f"{hlink('Ссылка', variant['Link'])}\n\n"

        view_actions_for_variants.add(types.InlineKeyboardButton(
            text=f"Просмотреть только для {key}",
            callback_data=f"{key}"))

    await ViewExchangeRate.MakeRequest.set()

    await call.message.edit_text(text, reply_markup=view_actions_for_variants)


# просмотр всех вариантов
@dp.callback_query_handler(text="view_all_variants", state=ViewExchangeRate.MakeRequest)
async def view_all_exchange_variants(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()
    response_data = data_state["data_exchange_variants"]

    text = ""
    view_actions_for_variants = types.InlineKeyboardMarkup(resize_keyboard=True)
    for key in response_data.keys():
        text += f"{key}\n\n"
        for variant in response_data[key]:
            text += f"Обменник {variant['Exchanger']}\n" \
                    f"Курс {variant['Rate']}\n" \
                    f"Рейтинг {variant['GoodReviews']}😀  {variant['BadReviews']}😡\n" \
                    f"{hlink('Ссылка', variant['Link'])}\n\n"

        view_actions_for_variants.add(types.InlineKeyboardButton(
            text=f"Просмотреть только для {key}",
            callback_data=f"{key}"))

    view_actions_for_variants.add(types.InlineKeyboardButton(
        text=f"Назад",
        callback_data="back"))

    await ViewExchangeRate.ViewAllVariants.set()

    await call.message.edit_text(text, reply_markup=view_actions_for_variants)


# просмотр только определенных вариантов
@dp.callback_query_handler(state=ViewExchangeRate.MakeRequest)
@dp.callback_query_handler(state=ViewExchangeRate.ViewAllVariants)
async def view_current_exchange_variants(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()
    response_data = data_state["data_exchange_variants"]

    text = ""
    view_actions_for_variants = types.InlineKeyboardMarkup(resize_keyboard=True)
    for key in response_data.keys():
        if key == call.data:
            text += f"{key}\n\n"
            for variant in response_data[key]:
                text += f"Обменник {variant['Exchanger']}\n" \
                        f"Курс {variant['Rate']}\n" \
                        f"Рейтинг {variant['GoodReviews']}😀  {variant['BadReviews']}😡\n" \
                        f"{hlink('Ссылка', variant['Link'])}\n\n"

    view_actions_for_variants.add(types.InlineKeyboardButton(
        text=f"Назад",
        callback_data="back"))

    await ViewExchangeRate.ViewCurrentVariants.set()

    await call.message.edit_text(text, reply_markup=view_actions_for_variants)
