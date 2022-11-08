import json
import pickle

import aioredis
from aiogram import types

from data import config
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


async def make_request_portfolio(user_id):
    data = {
        "telegramUserID": user_id,
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/portfolio/view"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    data_request = r.json()

    return data_request


async def make_request_for_find_currency_by_slug(user_id, slug):
    data = {
        "telegramUserID": user_id,
        "currency_name": "",
        "currency_slug": slug.upper()
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/search/try_find_currency"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    return r.json()


async def write_to_redis_portfolio(data_request, user_id):
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    await redis.set(f"portfolio_{user_id}", pickle.dumps(data_request))
    redis.close()
    await redis.wait_closed()


async def get_from_redis_portfolio(user_id):
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_portfolio = await redis.get(f"portfolio_{user_id}")
    data_portfolio = pickle.loads(data_portfolio)
    redis.close()
    await redis.wait_closed()

    return data_portfolio


async def make_text_and_keyboard_by_request_for_portfolio(data_request):
    currencies = []
    data_currencies = {}
    text = ""

    view_currency_in_portfolio_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_currency_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Добавить криптовалюту в портфель",
        callback_data="add_to_portfolio"))

    for currency in data_request:
        if currency['cryptocurrency'] not in currencies:
            currencies.append(currency['cryptocurrency'])
            if currency['type'] == "buy":
                data_currencies[f"{currency['cryptocurrency']}_price"] = float(currency['price'])
            else:
                data_currencies[f"{currency['cryptocurrency']}_price"] = float(currency['price']) * -1
            data_currencies[f"{currency['cryptocurrency']}_value"] = float(currency['value'])
            data_currencies[f"{currency['cryptocurrency']}_actualPrice"] = float(currency['actualPrice'])

            view_currency_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Перейти к {currency['cryptocurrency']}",
                callback_data=currency['cryptocurrency']))
        else:
            if currency['type'] == "buy":
                data_currencies[f"{currency['cryptocurrency']}_price"] += float(currency['price'])
                data_currencies[f"{currency['cryptocurrency']}_value"] += float(currency['value'])
            else:
                data_currencies[f"{currency['cryptocurrency']}_price"] -= float(currency['price'])
                data_currencies[f"{currency['cryptocurrency']}_value"] -= float(currency['value'])

    for currency in currencies:
        text += "<code>" + currency + "\nСтоимость:  " + str(
            data_currencies[f"{currency}_actualPrice"]) + "\nКоличество: " + \
                str(data_currencies[f"{currency}_value"]) + "</code>" + "\n\n"

    view_currency_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Просмотреть в webapp",
        web_app=types.WebAppInfo(url=f"{config.WEBHOOK_HOST}/portfolio")
    ))
    view_currency_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Вернуться в главное меню",
        callback_data="return_to_main_menu"
    ))
    view_currency_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Закрыть",
        callback_data="cancel"))

    return text, view_currency_in_portfolio_keyboard


async def make_text_and_keyboard_by_request_for_current_currency_in_portfolio(data_request, data_state):
    text = f"Записи по {data_state['current_currency_portfolio']}\n\n"
    view_currency_record_in_portfolio_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text=f"Добавить запись для {data_state['current_currency_portfolio']}",
        callback_data=f"add_record-{data_state['current_currency_portfolio']}"))

    for currency in data_request['result']:
        if currency['cryptocurrency'] == data_state['current_currency_portfolio']:
            text += f"<code>Цена добавления: {currency['price']}</code>\n" \
                    f"<code>Тип:             {currency['type']}</code>\n" \
                    f"<code>Количество:      {currency['value']}</code>\n" \
                    f"<code>Дата:            {currency['createdAt']}</code>\n\n"

            view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Перейти к записи {currency['createdAt']}",
                callback_data=f"record-{currency['id']}"))

    view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return text, view_currency_record_in_portfolio_keyboard
