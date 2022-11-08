import math
import pickle

import aioredis
from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.inline.view_index_rating_keyboards import view_type_of_index_rating_keyboard, \
    view_type_of_index_rating_from_main_menu_keyboard, view_web_app_link_keyboard, make_index_cb_keyboard
from loader import dp, bot
from states.view_index_rating import ViewIndexRating
from utils.func.index_rating import make_request_index_rating_by_page, make_text


@dp.message_handler(commands="index_rating", state="*")
async def index_rating_choose_type(message: types.Message, state: FSMContext):
    await message.answer("Выберите вариант отображения", reply_markup=view_type_of_index_rating_keyboard)

    await ViewIndexRating.StartChooseType.set()


@dp.callback_query_handler(text="view_index_rating_from_start_menu", state="*")
async def index_rating_default_cb(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите вариант отображения",
                                 reply_markup=view_type_of_index_rating_from_main_menu_keyboard)

    await ViewIndexRating.StartChooseType.set()


@dp.callback_query_handler(text="view_webapp_type", state=ViewIndexRating.StartChooseType)
async def index_rating_webapp(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Data",
                                 reply_markup=view_web_app_link_keyboard)


@dp.callback_query_handler(text="view_default_type", state=ViewIndexRating.StartChooseType)
async def index_rating_default(call: types.CallbackQuery, state: FSMContext):
    current_page = 1
    global_page = 1
    current_currency = "usd"
    current_period = "24h"

    async with state.proxy() as data:
        data['index_rating_global_page'] = global_page
        data['index_rating_current_page'] = current_page
        data['index_rating_current_currency'] = current_currency
        data['index_rating_current_period'] = current_period

    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_request = await redis.get(f"index_rating_page_{current_page}_{current_currency}")
    if data_request is not None:
        data_request = pickle.loads(data_request)
    redis.close()
    await redis.wait_closed()

    if data_request is None:
        data_request = await make_request_index_rating_by_page(call.from_user.id, global_page, current_currency)

    if data_request != "":
        text = await make_text(global_page, current_page, data_request, current_currency, current_period)

        await call.message.edit_text(text=text,
                                     reply_markup=await make_index_cb_keyboard(current_page))

    await ViewIndexRating.StartView.set()


@dp.callback_query_handler(text="next", state=ViewIndexRating.StartView)
async def next_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    # определяем страницу
    data_state = await state.get_data()
    current_page = data_state['index_rating_current_page'] + 1
    current_currency = data_state['index_rating_current_currency']
    current_period = data_state['index_rating_current_period']

    global_page = math.ceil(current_page / 25)

    async with state.proxy() as data:
        data['index_rating_global_page'] = global_page
        data['index_rating_current_page'] = current_page

    # проверяем наличие данных
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_request = await redis.get(f"index_rating_page_{global_page}_{current_currency}")
    if data_request is not None:
        data_request = pickle.loads(data_request)
    redis.close()
    await redis.wait_closed()

    if data_request is None:
        data_request = await make_request_index_rating_by_page(call.from_user.id, global_page, current_currency)

    if data_request != "":
        text = await make_text(global_page, current_page, data_request, current_currency, current_period)

        await call.message.edit_text(text=text,
                                     reply_markup=await make_index_cb_keyboard(current_page))


@dp.callback_query_handler(text="back", state=ViewIndexRating.StartView)
async def prev_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    # определяем страницу
    data_state = await state.get_data()
    current_page = data_state['index_rating_current_page'] - 1
    current_currency = data_state['index_rating_current_currency']
    current_period = data_state['index_rating_current_period']
    if current_page < 1:
        current_page += 1

    global_page = math.ceil(current_page / 25)

    async with state.proxy() as data:
        data['index_rating_global_page'] = global_page
        data['index_rating_current_page'] = current_page

    # проверяем наличие данных
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_request = await redis.get(f"index_rating_page_{global_page}_{current_currency}")
    if data_request is not None:
        data_request = pickle.loads(data_request)
    redis.close()
    await redis.wait_closed()

    if data_request is None:
        data_request = await make_request_index_rating_by_page(call.from_user.id, global_page, current_currency)

    if data_request != "":
        text = await make_text(global_page, current_page, data_request, current_currency, current_period)

        await call.message.edit_text(text=text,
                                     reply_markup=await make_index_cb_keyboard(current_page))


@dp.callback_query_handler(text="usd", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="btc", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="rub", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="eth", state=ViewIndexRating.StartView)
async def change_currency_page_to_call_data(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    # определяем страницу
    data_state = await state.get_data()
    current_page = data_state['index_rating_current_page']
    current_period = data_state['index_rating_current_period']
    global_page = math.ceil(current_page / 25)

    async with state.proxy() as data:
        data['index_rating_current_currency'] = call.data

    # проверяем наличие данных
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_request = await redis.get(f"index_rating_page_{global_page}_{call.data}")
    if data_request is not None:
        data_request = pickle.loads(data_request)
    redis.close()
    await redis.wait_closed()

    if data_request is None:
        data_request = await make_request_index_rating_by_page(call.from_user.id, global_page, call.data)

    if data_request != "":
        text = await make_text(global_page, current_page, data_request, call.data, current_period)

        await call.message.edit_text(text=text,
                                     reply_markup=await make_index_cb_keyboard(current_page))


@dp.callback_query_handler(text="24h", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="7d", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="30d", state=ViewIndexRating.StartView)
@dp.callback_query_handler(text="1y", state=ViewIndexRating.StartView)
async def change_period_to_call_data(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    # определяем страницу
    data_state = await state.get_data()
    current_page = data_state['index_rating_current_page']
    current_currency = data_state['index_rating_current_currency']
    current_period = call.data
    global_page = math.ceil(current_page / 25)

    async with state.proxy() as data:
        data['index_rating_current_period'] = current_period

    # проверяем наличие данных
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_request = await redis.get(f"index_rating_page_{global_page}_{current_currency}")
    if data_request is not None:
        data_request = pickle.loads(data_request)
    redis.close()
    await redis.wait_closed()

    if data_request is None:
        data_request = await make_request_index_rating_by_page(call.from_user.id, global_page, current_currency)

    if data_request != "":
        text = await make_text(global_page, current_page, data_request, current_currency, current_period)

        await call.message.edit_text(text=text,
                                     reply_markup=await make_index_cb_keyboard(current_page))


@dp.callback_query_handler(text="close_index_rating", state=ViewIndexRating.StartChooseType)
@dp.callback_query_handler(text="close_index_rating", state=ViewIndexRating.StartView)
async def close_index_trading(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await state.finish()
