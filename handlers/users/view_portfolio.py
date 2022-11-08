from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.view_portfolio_keyboards import view_actions_without_currencies_in_portfolio_keyboard, \
    view_actions_without_currencies_in_portfolio_from_main_menu_keyboard, \
    make_view_currency_after_find_request_keyboard, view_currency_after_find_request_no_results_keyboard, \
    make_view_currency_after_find_request_more_crypto_keyboard, view_actions_after_select_currency_keyboard, \
    view_actions_after_fill_data_keyboard, make_view_currency_record_in_portfolio_keyboard, \
    make_view_currencies_record_in_portfolio_keyboard, make_delete_confirmation_keyboard
from loader import dp, bot
from states.view_account_states import ViewAccountStates
from states.view_portfolio_states import ViewPortfolioStates
from states.view_trending_states import ViewTrendingStates
from utils.func.view_portfolio import make_request_portfolio, make_text_and_keyboard_by_request_for_portfolio, \
    write_to_redis_portfolio, get_from_redis_portfolio, \
    make_text_and_keyboard_by_request_for_current_currency_in_portfolio, make_request_for_find_currency_by_slug
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.message_handler(commands="portfolio", state="*")
@dp.message_handler(text="Портфель", state="*")
async def start_view_portfolio(message: types.Message):
    data_request = await make_request_portfolio(message.from_user.id)

    if data_request['result'] is not None:
        await write_to_redis_portfolio(data_request['result'], message.from_user.id)

        text, view_currency_in_portfolio_keyboard = await make_text_and_keyboard_by_request_for_portfolio(
            data_request['result'])

        await message.answer(
            "Вы можете выбрать определенную валюту для детального просмотра и редактирования\n\n" + text,
            reply_markup=view_currency_in_portfolio_keyboard)

        await ViewPortfolioStates.StartView.set()

    else:
        await message.answer("Ваш портфель сейчас пуст",
                             reply_markup=view_actions_without_currencies_in_portfolio_keyboard)

        await ViewPortfolioStates.AddCurrency.set()


@dp.callback_query_handler(text="view_my_portfolio", state=ViewAccountStates.StartView)
@dp.callback_query_handler(text="my_portfolio_from_start_menu", state="*")
async def start_view_portfolio_cb(call: types.CallbackQuery, state: FSMContext):
    data_request = await make_request_portfolio(call.from_user.id)

    if data_request['result'] is not None:
        await write_to_redis_portfolio(data_request['result'], call.from_user.id)

        text, view_currency_in_portfolio_keyboard = await make_text_and_keyboard_by_request_for_portfolio(
            data_request['result'])

        await call.message.edit_text(
            "Вы можете выбрать определенную валюту для детального просмотра и редактирования\n\n" + text,
            reply_markup=view_currency_in_portfolio_keyboard)

        await ViewPortfolioStates.StartView.set()

    else:
        await call.message.edit_text("Ваш портфель сейчас пуст",
                                     reply_markup=view_actions_without_currencies_in_portfolio_from_main_menu_keyboard)

        await ViewPortfolioStates.AddCurrency.set()


# добавить криптовалюту - отмена создания
@dp.callback_query_handler(text="cancel", state=ViewPortfolioStates.AddCurrency)
@dp.callback_query_handler(text="cancel", state=ViewPortfolioStates.StartView)
@dp.callback_query_handler(text="cancel", state=ViewPortfolioStates.ViewFinalData)
async def cancel_creation(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await state.finish()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


# добавить криптовалюту - ввод названия
@dp.callback_query_handler(text="add_to_portfolio", state=ViewPortfolioStates.AddCurrency)
@dp.callback_query_handler(text="add_to_portfolio", state=ViewPortfolioStates.StartView)
@dp.callback_query_handler(text="another_try", state=ViewPortfolioStates.FinishFindCurrency)
async def start_add_currency_to_portfolio(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Введите название интересующей вас валюты")

    await ViewPortfolioStates.FindCurrency.set()


# добавить криптовалюту - выбор
@dp.message_handler(state=ViewPortfolioStates.FindCurrency)
async def find_currency_for_add(message: types.Message):
    data_request = await make_request_for_find_currency_by_slug(message.from_user.id, message.text)

    if data_request['result'] is not None:
        await message.answer("Выберите интересующую вас криптовалюту.",
                             reply_markup=await make_view_currency_after_find_request_keyboard(
                                 data_request['result']['coins'], message.text))
    else:
        await message.answer("Интересующая вас криптовалюта не найдена",
                             reply_markup=view_currency_after_find_request_no_results_keyboard)

    await ViewPortfolioStates.FinishFindCurrency.set()


# добавить криптовалюту - выбор расширенный
@dp.callback_query_handler(text_startswith="more_crypto-", state=ViewPortfolioStates.FinishFindCurrency)
async def find_currency_for_add_cb(call: types.CallbackQuery, state: FSMContext):
    data_request = await make_request_for_find_currency_by_slug(call.from_user.id,
                                                                call.data.replace('more_crypto-', ''))

    if data_request['result'] is not None:
        await call.message.edit_text("Выберите интересующую вас криптовалюту.",
                                     reply_markup=await make_view_currency_after_find_request_more_crypto_keyboard(
                                         data_request['result']['coins']))
    else:
        await call.message.edit_text("Интересующая вас криптовалюта не найдена",
                                     reply_markup=view_currency_after_find_request_no_results_keyboard)

    await ViewPortfolioStates.FinishFindCurrency.set()


# добавить криптовалюту - ввод количества
@dp.callback_query_handler(text_startswith="currency-", state=ViewPortfolioStates.FinishFindCurrency)
@dp.callback_query_handler(text_startswith="add_record-", state=ViewPortfolioStates.StartViewCurrency)
@dp.callback_query_handler(text_startswith="add_to_portfolio-",
                           state=ViewTrendingStates.SendBasicInfoOfTrendingCurrency)
async def count_of_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        if "add_record-" in call.data:
            data['data_for_add_in_portfolio_currency'] = call.data.replace("add_record-", "")
        elif "currency-" in call.data:
            data['data_for_add_in_portfolio_currency'] = call.data.replace("currency-", "")
        elif "add_to_portfolio-" in call.data:
            data['data_for_add_in_portfolio_currency'] = call.data.replace("add_to_portfolio-", "").upper()

    await call.message.edit_text(text="Выберите тип - продажа или покупка",
                                 reply_markup=view_actions_after_select_currency_keyboard)

    await ViewPortfolioStates.Type.set()


# добавить криптовалюту - ввод количества
@dp.callback_query_handler(state=ViewPortfolioStates.Type)
async def count_of_currency(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['data_for_add_in_portfolio_type'] = call.data

    await call.message.edit_text(text="Введите количество криптовалюты")

    await ViewPortfolioStates.CountOfCurrency.set()


# добавить криптовалюту - ввод цены
@dp.message_handler(state=ViewPortfolioStates.CountOfCurrency)
async def price_of_currency(message: types.Message, state: FSMContext):
    try:
        value = float(message.text)

        if value <= 0:
            raise ValueError

        async with state.proxy() as data:
            data['data_for_add_in_portfolio_currency_count'] = value

        await message.answer(text="Введите цену криптовалюту в USD (по которой вы купили)")

        await ViewPortfolioStates.PriceOfCurrency.set()
    except ValueError:
        await message.answer(text="Вы ввели не корректное число. Попробуйте еще раз")

        await ViewPortfolioStates.CountOfCurrency.set()


# добавить криптовалюту - просмотр записи
@dp.message_handler(state=ViewPortfolioStates.PriceOfCurrency)
async def view_finish_data(message: types.Message, state: FSMContext):
    try:
        value = float(message.text)

        if value <= 0:
            raise ValueError

        async with state.proxy() as data:
            data['data_for_add_in_portfolio_currency_price'] = message.text

        data_state = await state.get_data()

        await message.answer(text=f"Итоговый просмотр\n\n"
                                  f"<code>Валюта:     {data_state['data_for_add_in_portfolio_currency']}</code>\n"
                                  f"<code>Количество: {data_state['data_for_add_in_portfolio_currency_count']}</code>\n"
                                  f"<code>Тип:        {data_state['data_for_add_in_portfolio_type']}</code>\n"
                                  f"<code>Цена:       {message.text}</code>",
                             reply_markup=view_actions_after_fill_data_keyboard)

        await ViewPortfolioStates.ViewFinalData.set()
    except ValueError:
        await message.answer(text="Вы ввели не корректное число. Попробуйте еще раз")

        await ViewPortfolioStates.PriceOfCurrency.set()


# добавить криптовалюту - закончить создание
@dp.callback_query_handler(text="confirm", state=ViewPortfolioStates.ViewFinalData)
async def confirm_creation(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "cryptocurrency": data_state['data_for_add_in_portfolio_currency'],
        "value": float(data_state['data_for_add_in_portfolio_currency_count']),
        "price": float(data_state['data_for_add_in_portfolio_currency_price']),
        "type": str(data_state['data_for_add_in_portfolio_type'])
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/portfolio/add"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] == "ok":
        data_request = await make_request_portfolio(call.from_user.id)

        if data_request['result'] is not None:
            await write_to_redis_portfolio(data_request['result'], call.from_user.id)

            text, view_currency_in_portfolio_keyboard = await make_text_and_keyboard_by_request_for_portfolio(
                data_request['result'])

            await call.message.edit_text(
                "Вы можете выбрать определенную валюту для детального просмотра и редактирования\n\n" + text,
                reply_markup=view_currency_in_portfolio_keyboard)

            await ViewPortfolioStates.StartView.set()

        else:
            await call.message.edit_text("Ваш портфель сейчас пуст",
                                         reply_markup=view_actions_without_currencies_in_portfolio_keyboard)

            await ViewPortfolioStates.AddCurrency.set()

    else:
        await call.message.edit_text("Что-то пошло не так. Попробуйте позже")


# просмотр конкретной криптовалюту
@dp.callback_query_handler(state=ViewPortfolioStates.StartView)
@dp.callback_query_handler(text_startswith="back-", state=ViewPortfolioStates.StartViewRecord)
@dp.callback_query_handler(text_startswith="cancel_delete-", state=ViewPortfolioStates.StartDeleteRecord)
async def view_selected_currency_in_portfolio(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_portfolio = await get_from_redis_portfolio(call.from_user.id)

    if "back-" in call.data:
        call.data = call.data.replace("back-", "")
    elif "cancel_delete-" in call.data:
        call.data = call.data.replace("cancel_delete-", "")

    async with state.proxy() as data:
        data['current_currency_portfolio'] = call.data

    keyboard, text = await make_view_currencies_record_in_portfolio_keyboard(data_portfolio, call.data)

    await call.message.edit_text(text=text,
                                 reply_markup=keyboard)

    await ViewPortfolioStates.StartViewCurrency.set()


# просмотр конкретной записи
@dp.callback_query_handler(text_startswith="record-", state=ViewPortfolioStates.StartViewCurrency)
async def view_current_record_in_portfolio(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_portfolio = await get_from_redis_portfolio(call.from_user.id)

    id_record = call.data.replace("record-", "")
    keyboard, text = await make_view_currency_record_in_portfolio_keyboard(data_portfolio, id_record)

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard)

    await ViewPortfolioStates.StartViewRecord.set()


# изменение количества монет в записи
@dp.callback_query_handler(text_startswith="change_count_record-", state=ViewPortfolioStates.StartViewRecord)
async def get_count_for_change_record(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['current_order_id'] = call.data.replace("change_count_record-", "")

    await call.message.edit_text(text="Введите количество на которое изменить")

    await ViewPortfolioStates.StartChangeCountRecord.set()


@dp.message_handler(state=ViewPortfolioStates.StartChangeCountRecord)
async def change_count_record(message: types.Message, state: FSMContext):
    try:
        value_x = float(message.text)

        if value_x >= 0:
            data_state = await state.get_data()

            data = {
                "telegramUserID": message.from_user.id,
                "record_id": data_state['current_order_id'],
                "value": float(message.text),
                "price": 0
            }
            token = await generate_token(data)
            endpoint = f"http://127.0.0.1:8080/api/account/portfolio/update"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            r = await make_request_get(endpoint, headers)

            if r.json()['result'] == 'ok':
                data_request = await make_request_portfolio(message.from_user.id)

                if data_request['result'] is not None:
                    await write_to_redis_portfolio(data_request['result'], message.from_user.id)

                    text, view_currency_record_in_portfolio_keyboard = \
                        await make_text_and_keyboard_by_request_for_current_currency_in_portfolio(data_request,
                                                                                                  data_state)

                    await message.answer(text=text, reply_markup=view_currency_record_in_portfolio_keyboard)

                    await ViewPortfolioStates.StartViewCurrency.set()

                else:
                    await message.answer("Что-то пошло не так")

            else:
                await message.answer("Что-то пошло не так")

        else:
            await message.answer(text="Введеное число меньше нуля, попробуйте еще раз")

            await ViewPortfolioStates.StartChangeCountRecord.set()

    except ValueError:
        await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

        await ViewPortfolioStates.StartChangeCountRecord.set()


# изменение цены в записи
@dp.callback_query_handler(text_startswith="change_price_record-", state=ViewPortfolioStates.StartViewRecord)
async def get_price_for_change_record(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['current_order_id'] = call.data.replace("change_price_record-", "")

    await call.message.edit_text(text="Введите цену на которую изменить")

    await ViewPortfolioStates.StartChangePriceRecord.set()


@dp.message_handler(state=ViewPortfolioStates.StartChangePriceRecord)
async def change_price_record(message: types.Message, state: FSMContext):
    try:
        value_x = float(message.text)

        if value_x >= 0:
            data_state = await state.get_data()

            data = {
                "telegramUserID": message.from_user.id,
                "record_id": data_state['current_order_id'],
                "value": 0,
                "price": float(message.text)
            }
            token = await generate_token(data)
            endpoint = f"http://127.0.0.1:8080/api/account/portfolio/update"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            r = await make_request_get(endpoint, headers)

            if r.json()['result'] == 'ok':
                data_request = await make_request_portfolio(message.from_user.id)

                if data_request['result'] is not None:
                    await write_to_redis_portfolio(data_request['result'], message.from_user.id)

                    text, view_currency_record_in_portfolio_keyboard = \
                        await make_text_and_keyboard_by_request_for_current_currency_in_portfolio(data_request,
                                                                                                  data_state)

                    await message.answer(text=text, reply_markup=view_currency_record_in_portfolio_keyboard)

                    await ViewPortfolioStates.StartViewCurrency.set()

                else:
                    await message.answer("Что-то плошло не так")

            else:
                await message.answer("Что-то пошло не так")

        else:
            await message.answer(text="Введеное число меньше нуля, попробуйте еще раз")

            await ViewPortfolioStates.StartChangePriceRecord.set()

    except ValueError:
        await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

        await ViewPortfolioStates.StartChangePriceRecord.set()


# удаление записи
@dp.callback_query_handler(text_startswith="delete_record-", state=ViewPortfolioStates.StartViewRecord)
async def delete_record(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        data['current_order_id'] = call.data.replace("delete_record-", "")

    await call.message.edit_text(text="Введите количество на которое изменить",
                                 reply_markup=await make_delete_confirmation_keyboard(data['current_currency_portfolio']))

    await ViewPortfolioStates.StartDeleteRecord.set()


@dp.callback_query_handler(text="confirm_delete", state=ViewPortfolioStates.StartDeleteRecord)
async def delete_record_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "record_id": data_state['current_order_id'],
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/portfolio/delete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] == "ok":
        data_request = await make_request_portfolio(call.from_user.id)

        if data_request['result'] is not None:
            await write_to_redis_portfolio(data_request['result'], call.from_user.id)

            text, view_currency_record_in_portfolio_keyboard = \
                await make_text_and_keyboard_by_request_for_current_currency_in_portfolio(data_request, data_state)

            await call.message.edit_text(text=text, reply_markup=view_currency_record_in_portfolio_keyboard)

            await ViewPortfolioStates.StartViewCurrency.set()

        else:
            await call.message.edit_text(text="Что-то пошло не так")
    else:
        await call.message.edit_text(text="Что-то пошло не так")


# вернуться назад от просмотра записей
@dp.callback_query_handler(text="back", state=ViewPortfolioStates.StartViewCurrency)
@dp.callback_query_handler(text="back", state=ViewPortfolioStates.FinishFindCurrency)
async def back_to_portfolio_main_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_portfolio = await get_from_redis_portfolio(call.from_user.id)

    text, view_currency_in_portfolio_keyboard = await make_text_and_keyboard_by_request_for_portfolio(data_portfolio)

    await call.message.edit_text(
        "Вы можете выбрать определенную валюту для детального просмотра и редактирования\n\n" + text,
        reply_markup=view_currency_in_portfolio_keyboard)

    await ViewPortfolioStates.StartView.set()
