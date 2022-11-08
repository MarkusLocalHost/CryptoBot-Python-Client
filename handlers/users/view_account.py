from aiogram import types
from aiogram.dispatcher import FSMContext
from dateutil.parser import parse

from keyboards.inline.view_account_keyboards import make_action_in_account_keyboard, \
    make_view_action_after_receiving_observers_keyboard, make_view_action_after_receiving_current_observer_keyboard, \
    view_action_after_delete_observer_keyboard, view_action_after_view_subscription_keyboard, \
    view_action_in_enter_promo_code_keyboard, view_action_after_enter_promo_code_keyboard, \
    make_view_action_after_receiving_current_percentage_observer, make_view_action_after_receiving_percentage_observers
from loader import dp, bot
from states.view_account_states import ViewAccountStates
from utils.misc.requests_type import make_request_get
from utils.token.token import *


@dp.message_handler(commands="account", state="*")
@dp.message_handler(text="Мой аккаунт", state="*")
async def account_view_action(message: types.Message):
    await message.answer("Выберите интересующее вас действие.\n"
                         "Тип подписки и лимиты вы можете посмотреть в пункте 'Подписки и лимиты'",
                         reply_markup=await make_action_in_account_keyboard(False))

    await ViewAccountStates.StartView.set()


@dp.callback_query_handler(text="back", state=ViewAccountStates.ViewObservers)
@dp.callback_query_handler(text="back", state=ViewAccountStates.ViewPercentageObserver)
@dp.callback_query_handler(text="back", state=ViewAccountStates.ViewAccountSubscription)
@dp.callback_query_handler(text="my_account_from_start_menu", state="*")
async def account_view_action_cb_from_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text("Выберите интересующее вас действие.\n"
                                 "Тип подписки и лимиты вы можете посмотреть в пункте 'Подписки и лимиты'",
                                 reply_markup=await make_action_in_account_keyboard(True))

    await ViewAccountStates.StartView.set()


# работа с обсерверами
@dp.callback_query_handler(text="back", state=ViewAccountStates.ViewCurrentObserver)
@dp.callback_query_handler(text="return_to_observers", state=ViewAccountStates.DeleteCurrentObserver)
@dp.callback_query_handler(text="return_to_observers", state=ViewAccountStates.ChangeStatusCurrentObserver)
@dp.callback_query_handler(text="view_my_observers", state=ViewAccountStates.StartView)
@dp.callback_query_handler(text="next", state=ViewAccountStates.ViewObservers)
@dp.callback_query_handler(text="prev", state=ViewAccountStates.ViewObservers)
async def account_view_observers(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    if call.data == "view_my_observers" or call.data == "return_to_observers":
        data = {
            "telegramUserID": call.from_user.id,
        }
        token = await generate_token(data)
        endpoint = f"http://127.0.0.1:8080/api/account/price_observers/list"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        r = await make_request_get(endpoint, headers)
        data_request = r.json()['result']

        async with state.proxy() as data:
            data['view_price_observers_current_page'] = 1
            data['account_observers'] = data_request
    elif call.data == "back":
        data = await state.get_data()
    elif call.data == "next":
        async with state.proxy() as data:
            data['view_price_observers_current_page'] += 1
    else:
        async with state.proxy() as data:
            data['view_price_observers_current_page'] -= 1

    view_action_after_receiving_observers = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_action_after_receiving_observers.add(types.InlineKeyboardButton(
        text="Создать обсервер",
        callback_data="create_observer"))

    if data['account_observers'] is not None:
        keyboard, text = await make_view_action_after_receiving_observers_keyboard(data['account_observers'], data[
            'view_price_observers_current_page'])

        await call.message.edit_text("Выберите обсервер для подробной информации и действий с ним.\n\n" + text,
                                     reply_markup=keyboard)
    else:
        # обработать
        view_action_after_receiving_observers.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back"))

        await call.message.edit_text("Обсерверы не найдены",
                                     reply_markup=view_action_after_receiving_observers)

    await ViewAccountStates.ViewObservers.set()


@dp.callback_query_handler(text_startswith="observer", state=ViewAccountStates.ViewObservers)
async def account_view_current_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    keyboard, text = await make_view_action_after_receiving_current_observer_keyboard(data_state['account_observers'],
                                                                                      call, state)

    await call.message.edit_text(text,
                                 reply_markup=keyboard)

    await ViewAccountStates.ViewCurrentObserver.set()


@dp.callback_query_handler(text="delete", state=ViewAccountStates.ViewCurrentObserver)
async def account_delete_current_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "observerID": data_state['selected_observer']
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/price_observers/delete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text("Обсервер успешно удален",
                                     reply_markup=view_action_after_delete_observer_keyboard)

        await ViewAccountStates.DeleteCurrentObserver.set()
    else:
        # обработать
        await call.message.edit_text("Произошла ошибка")


@dp.callback_query_handler(text="deactivate", state=ViewAccountStates.ViewCurrentObserver)
@dp.callback_query_handler(text="activate", state=ViewAccountStates.ViewCurrentObserver)
async def account_change_status_current_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "observerID": data_state['selected_observer']
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/price_observers/change_status"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        text = ""
        if r.json()['result'] == "observer stopped":
            text = "Обсервер успешно остановлен"
        elif r.json()['result'] == "observer started":
            text = "Обсервер успешно запущен"
        elif r.json()['result'] == "limit reached":
            text = "Обсервер не может быть запущен из-за лимитов"

        await call.message.edit_text(text,
                                     reply_markup=view_action_after_delete_observer_keyboard)

        await ViewAccountStates.ChangeStatusCurrentObserver.set()
    else:
        # обработать
        await call.message.edit_text("Произошла ошибка")


# просмотр обсерверов на проценты
@dp.callback_query_handler(text="back", state=ViewAccountStates.ViewCurrentPercentageObserver)
@dp.callback_query_handler(text="return_to_observers", state=ViewAccountStates.DeleteCurrentPercentageObserver)
@dp.callback_query_handler(text="view_my_percentage_observers", state=ViewAccountStates.StartView)
async def account_view_percentage_observers(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data = {
        "telegramUserID": call.from_user.id,
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/percentage_observers/list"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    view_action_after_receiving_percentage_observers = types.InlineKeyboardMarkup(resize_keyboard=True)

    if r.json()['result'] is not None:
        async with state.proxy() as data:
            data['account_percentage_observers'] = r.json()['result']

        keyboard, text = await make_view_action_after_receiving_percentage_observers(
            r.json()['result'],
            call, state)

        await call.message.edit_text("Выберите обсервер для подробной информации и действий с ним.\n\n" + text,
                                     reply_markup=keyboard,
                                     parse_mode="")
    else:
        # обработать
        view_action_after_receiving_percentage_observers.add(types.InlineKeyboardButton(
            text="Создать обсервер",
            callback_data="create_percent_observer_from_account"))
        view_action_after_receiving_percentage_observers.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back"))

        await call.message.edit_text("Обсерверы не найдены",
                                     reply_markup=view_action_after_receiving_percentage_observers)

    await ViewAccountStates.ViewPercentageObserver.set()


@dp.callback_query_handler(state=ViewAccountStates.ViewPercentageObserver)
async def account_view_current_percentage_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    keyboard, text = await make_view_action_after_receiving_current_percentage_observer(
        data_state['account_percentage_observers'],
        call, state)

    await call.message.edit_text(text,
                                 reply_markup=keyboard,
                                 parse_mode="")

    await ViewAccountStates.ViewCurrentPercentageObserver.set()


@dp.callback_query_handler(text="delete", state=ViewAccountStates.ViewCurrentPercentageObserver)
async def account_delete_current_percentage_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "observerID": data_state['selected_percentage_observer']
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/percentage_observer/delete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text("Обсервер успешно удален",
                                     reply_markup=view_action_after_delete_observer_keyboard)

        await ViewAccountStates.DeleteCurrentPercentageObserver.set()
    else:
        # обработать
        await call.message.edit_text("Произошла ошибка")


# работа с подпиской
@dp.callback_query_handler(text="view_my_subscription", state=ViewAccountStates.StartView)
@dp.callback_query_handler(text="back", state=ViewAccountStates.EnterPromoCode)
@dp.callback_query_handler(text="back", state=ViewAccountStates.IncorrectPromoCode)
async def account_view_subscription(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data = {
        "telegramUserID": call.from_user.id,
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/subscription/view"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] is not None:
        await call.message.edit_text(f"Ваша подписка {r.json()['result']['subscriptionType']}\n"
                                     f"Количество активных обсерверов Tier1 {r.json()['result']['count_observers_tier1']} из {r.json()['result']['limit_observers_tier1']} возможных\n"
                                     f"Количество активных обсерверов Tier2 {r.json()['result']['count_observers_tier2']} из {r.json()['result']['limit_observers_tier2']} возможных\n"
                                     f"Периодичность работы обсервера: {r.json()['result']['time_to_observe']} сек.\n"
                                     f"Количество активных обсерверов на проценты {r.json()['result']['count_observers_percentage']} из {r.json()['result']['limit_observers_percentage']} возможных",
                                     reply_markup=view_action_after_view_subscription_keyboard)

        await ViewAccountStates.ViewAccountSubscription.set()
    else:
        # обработать
        await call.message.edit_text("Произошла ошибка")


@dp.callback_query_handler(text="promocode", state=ViewAccountStates.ViewAccountSubscription)
@dp.callback_query_handler(text="retry_promo_code", state=ViewAccountStates.IncorrectPromoCode)
async def enter_promo_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text("Введите промокод", reply_markup=view_action_in_enter_promo_code_keyboard)

    await ViewAccountStates.EnterPromoCode.set()


@dp.message_handler(state=ViewAccountStates.EnterPromoCode)
async def result_of_enter_promo_code(message: types.Message, state: FSMContext):
    data = {
        "telegramUserID": message.from_user.id,
        "promoCode": message.text
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/promo_code/check"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    try:
        if r.json()["result"] == "time of active is ended":
            await message.answer("Время действия промокода истекло",
                                 reply_markup=view_action_after_enter_promo_code_keyboard)

            await ViewAccountStates.IncorrectPromoCode.set()

        elif r.json()["result"] == "you already activate this promo code":
            await message.answer("Вы уже активировали этот промокод",
                                 reply_markup=view_action_after_enter_promo_code_keyboard)

            await ViewAccountStates.IncorrectPromoCode.set()

        elif r.json()["result"] == "limit of activation":
            await message.answer("Лимит использований проомокода исчерпан",
                                 reply_markup=view_action_after_enter_promo_code_keyboard)

            await ViewAccountStates.IncorrectPromoCode.set()

        elif r.json()["result"] == "no promo code in db":
            await message.answer("Такого промокода не существует",
                                 reply_markup=view_action_after_enter_promo_code_keyboard)

            await ViewAccountStates.IncorrectPromoCode.set()

        elif r.json()["result"] == "promo code activated":
            data = {
                "telegramUserID": message.from_user.id,
            }
            token = await generate_token(data)
            endpoint = f"http://127.0.0.1:8080/api/account/subscription/view"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            r = await make_request_get(endpoint, headers)

            if r.json()['result'] is not None:
                await message.answer(f"Ваша подписка {r.json()['result']['subscriptionType']}\n"
                                     f"Количество активных обсерверов Tier1 {r.json()['result']['count_observers_tier1']} из {r.json()['result']['limit_observers_tier1']} возможных\n"
                                     f"Количество активных обсерверов Tier2 {r.json()['result']['count_observers_tier2']} из {r.json()['result']['limit_observers_tier2']} возможных\n"
                                     f"Количество активных обсерверов на проценты {r.json()['result']['count_observers_percentage']} из {r.json()['result']['limit_observers_percentage']} возможных",
                                     reply_markup=view_action_after_view_subscription_keyboard)

                await ViewAccountStates.ViewAccountSubscription.set()
            else:
                # обработать
                await message.answer("Произошла ошибка")

        else:
            await message.answer("Произошла ошибка")
    except KeyError:
        await message.answer("Произошла ошибка")


# закрыть меню
@dp.callback_query_handler(text="close_account", state=ViewAccountStates.StartView)
@dp.callback_query_handler(text="close_account", state=ViewAccountStates.DeleteCurrentObserver)
@dp.callback_query_handler(text="close_account", state=ViewAccountStates.DeleteCurrentPercentageObserver)
@dp.callback_query_handler(text="close_account", state=ViewAccountStates.ChangeStatusCurrentObserver)
async def close_account_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await state.finish()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
