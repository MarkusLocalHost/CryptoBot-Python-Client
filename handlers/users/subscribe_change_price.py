from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.subscribe_change_price_keyboards import subscribe_change_price_keyboard, \
    subscribe_change_price_from_main_menu_keyboard, change_next_settings_keyboard, \
    make_subscribe_change_price_settings_keyboard, make_set_next_action_after_first_filter_keyboard, \
    set_next_action_after_second_filter_keyboard, view_action_after_create_percentage_observer
from loader import dp, bot
from states.subscribe_change_price_states import SubscribeChangePriceStates
from states.view_account_states import ViewAccountStates
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


@dp.message_handler(commands="subscribe_change_price", state="*")
async def subscribe_change_price(message: types.Message):
    await message.answer(
        "Вы можете подписаться на отслеживание цены первых 1000 по капитализации криптовалют"
        " за небольшие промежутки (20, 40, 60 минут)\n",
        reply_markup=subscribe_change_price_keyboard)

    await SubscribeChangePriceStates.StartSubscribe.set()


@dp.callback_query_handler(text="create_percent_observer_from_start_menu", state="*")
@dp.callback_query_handler(text="create_percent_observer_from_account", state=ViewAccountStates.ViewPercentageObserver)
async def subscribe_change_price_cb(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Вы можете подписаться на отслеживание цены первых 1000 по капитализации криптовалют"
        " за небольшие промежутки (20, 40, 60 минут)\n",
        reply_markup=subscribe_change_price_from_main_menu_keyboard)

    await SubscribeChangePriceStates.StartSubscribe.set()


# настройки
@dp.callback_query_handler(text="settings", state=SubscribeChangePriceStates.StartSubscribe)
async def change_settings(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    min_20_is_active = False
    min_60_is_active = False
    async with state.proxy() as data_state:
        data_state['min_20_is_active'] = False
        data_state['min_60_is_active'] = False
        data_state['type_filter_first'] = ""
        data_state['x_filter_first'] = 0
        data_state['type_filter_second'] = ""
        data_state['x_filter_second'] = 0

    await call.message.edit_text(text="Выберите  настройки по периодичности отслеживания изменения цен",
                                 reply_markup=await make_subscribe_change_price_settings_keyboard(min_20_is_active,
                                                                                                  min_60_is_active))

    await SubscribeChangePriceStates.Settings.set()


@dp.callback_query_handler(text="activate_20_minutes", state=SubscribeChangePriceStates.Settings)
@dp.callback_query_handler(text="deactivate_20_minutes", state=SubscribeChangePriceStates.Settings)
@dp.callback_query_handler(text="activate_60_minutes", state=SubscribeChangePriceStates.Settings)
@dp.callback_query_handler(text="deactivate_60_minutes", state=SubscribeChangePriceStates.Settings)
@dp.callback_query_handler(text="back_settings", state=SubscribeChangePriceStates.FilterSettings)
async def change_settings(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    if call.data == "activate_20_minutes":
        data_state["min_20_is_active"] = True
    elif call.data == "deactivate_20_minutes":
        data_state["min_20_is_active"] = False
    elif call.data == "activate_60_minutes":
        data_state["min_60_is_active"] = True
    elif call.data == "deactivate_60_minutes":
        data_state["min_60_is_active"] = False

    async with state.proxy() as data:
        data['min_20_is_active'] = data_state["min_20_is_active"]
        data['min_60_is_active'] = data_state["min_60_is_active"]

    await call.message.edit_text(text="Выберите настройки по периодичности отслеживания изменения цен",
                                 reply_markup=await
                                 make_subscribe_change_price_settings_keyboard(data_state["min_20_is_active"],
                                                                               data_state["min_60_is_active"]))

    await SubscribeChangePriceStates.Settings.set()


@dp.callback_query_handler(text="next_settings", state=SubscribeChangePriceStates.Settings)
async def change_filter_settings(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Выберите фильтр для результатов",
                                 reply_markup=change_next_settings_keyboard)

    await SubscribeChangePriceStates.FilterSettings.set()


@dp.callback_query_handler(text="percent_smaller", state=SubscribeChangePriceStates.FilterSettings)
@dp.callback_query_handler(text="percent_bigger", state=SubscribeChangePriceStates.FilterSettings)
async def receive_x_for_filter_settings(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    type_filter = ""

    if call.data == "percent_smaller":
        type_filter = "percent_smaller"
    elif call.data == "percent_bigger":
        type_filter = "percent_bigger"

    async with state.proxy() as data_state:
        data_state["type_filter_first"] = type_filter

    await call.message.edit_text(text="Введите число для x для фильтра.\n"
                                      "Число должно быть положительным, дробная часть должна отделяться точкой.")

    await SubscribeChangePriceStates.ReceiveXForFilter.set()


@dp.message_handler(state=SubscribeChangePriceStates.ReceiveXForFilter)
async def set_next_action_after_first_filter(message: types.Message, state: FSMContext):
    try:
        value_x = float(message.text)

        if value_x >= 0:
            data_state = await state.get_data()

            async with state.proxy() as data_state:
                data_state["x_filter_first"] = value_x

            await message.answer(text="Выберите дальнейшее действие. Закончить создание или добавить еще один фильтр",
                                 reply_markup=await make_set_next_action_after_first_filter_keyboard(
                                     data_state["type_filter_first"]))

            await SubscribeChangePriceStates.SecondFilterSettings.set()
        else:
            await message.answer(text="Введеное число меньше нуля, попробуйте еще раз")

            await SubscribeChangePriceStates.ReceiveXForFilter.set()

    except ValueError:
        await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

        await SubscribeChangePriceStates.ReceiveXForFilter.set()


@dp.callback_query_handler(text="percent_smaller", state=SubscribeChangePriceStates.SecondFilterSettings)
@dp.callback_query_handler(text="percent_bigger", state=SubscribeChangePriceStates.SecondFilterSettings)
async def receive_x_for_second_filter_settings(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    type_filter = ""

    if call.data == "percent_smaller":
        type_filter = "percent_smaller"
    elif call.data == "percent_bigger":
        type_filter = "percent_bigger"

    async with state.proxy() as data_state:
        data_state["type_filter_second"] = type_filter

    await call.message.edit_text(text="Введите число для x для фильтра.\n"
                                      "Число должно быть положительным, дробная часть должна отделяться точкой.")

    await SubscribeChangePriceStates.ReceiveSecondXForFilter.set()


@dp.message_handler(state=SubscribeChangePriceStates.ReceiveSecondXForFilter)
async def set_next_action_after_second_filter(message: types.Message, state: FSMContext):
    try:
        value_x = float(message.text)

        if value_x >= 0:
            async with state.proxy() as data_state:
                data_state["x_filter_second"] = value_x

            # todo если большее меньше меньшего в сравнении процента

            await message.answer(text=f"Просмотр характеристик\n"
                                      f"{data_state['min_20_is_active']}\n"
                                      f"{data_state['min_60_is_active']}\n"
                                      f"{data_state['type_filter_first']}\n"
                                      f"{data_state['x_filter_second']}\n"
                                      f"{data_state['type_filter_second']}\n"
                                      f"{data_state['x_filter_second']}\n",
                                 reply_markup=set_next_action_after_second_filter_keyboard)

            await SubscribeChangePriceStates.ViewInfo.set()
        else:
            await message.answer(text="Введеное число меньше нуля, попробуйте еще раз")

            await SubscribeChangePriceStates.ReceiveSecondXForFilter.set()
    except ValueError:
        await message.answer(text="Введеный набор символов не является числом, попробуйте еще раз")

        await SubscribeChangePriceStates.ReceiveSecondXForFilter.set()


@dp.callback_query_handler(text="finish", state=SubscribeChangePriceStates.FilterSettings)
@dp.callback_query_handler(text="finish", state=SubscribeChangePriceStates.SecondFilterSettings)
@dp.callback_query_handler(text="finish", state=SubscribeChangePriceStates.ViewInfo)
async def finish_make_percentage_observer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data_state = await state.get_data()

    data = {
        "telegramUserID": call.from_user.id,
        "observe20Minutes": data_state['min_20_is_active'],
        "observe60Minutes": data_state['min_60_is_active'],
        "firstFilterType": data_state['type_filter_first'],
        "firstFilterAmount": data_state['x_filter_first'],
        "secondFilterType": data_state['type_filter_second'],
        "secondFilterAmount": data_state['x_filter_second'],
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/observers/percentage_observer/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] == "observer created and started":
        await call.message.edit_text(f"Обсервер успешно создан и запущен",
                                     reply_markup=view_action_after_create_percentage_observer)

        await state.finish()

    elif r.json()['result'] == "observer not created because limits":
        await call.message.edit_text(f"У вас превышено лимит количества обсерверов на проценты",
                                     reply_markup=view_action_after_create_percentage_observer)

        await state.finish()

    else:
        await call.message.edit_text(f"Произошла ошибка")

        await state.finish()


# отмена
@dp.callback_query_handler(text="close_settings", state=SubscribeChangePriceStates.Settings)
@dp.callback_query_handler(text="close_settings", state=SubscribeChangePriceStates.SecondFilterSettings)
@dp.callback_query_handler(text="cancel_subscribe", state=SubscribeChangePriceStates.StartSubscribe)
@dp.callback_query_handler(text="cancel_subscribe", state=SubscribeChangePriceStates.FilterSettings)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)

    await state.finish()
