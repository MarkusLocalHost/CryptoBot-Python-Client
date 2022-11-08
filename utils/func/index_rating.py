import pickle

import aioredis

from data import config
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


async def make_request_index_rating_by_page(user_id, page, currency):
    data = {
        "telegramUserID": user_id,
        "page": page,
        "currency": currency
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/info/index_rating"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    data_request = r.json()

    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    # определить время жизни
    await redis.set(f"index_rating_page_{page}_{currency}", pickle.dumps(data_request), expire=600)
    redis.close()
    await redis.wait_closed()

    return data_request


async def make_text(global_page, current_page, data_request, current_currency, current_period):
    number = (global_page - 1) * 250 + 10 * (current_page - (global_page - 1) * 25 - 1)
    text = f"<code>Криптовалюты {1 + number} - {10 + number} {current_currency.upper()} {current_period}</code>\n" \
           f"<code>#    Валюта       Цена   Изм.</code>\n"

    for i in range(10):
        d = i + (current_page - (global_page - 1) * 25 - 1) * 10

        string_number = str(d + 1) + " " * (5 - len(str(d + 1)))

        string_slug = " " * (5 - len(data_request['result'][d]['symbol'])) + data_request['result'][d]['symbol']

        string_price = " " * (10 - len(str(data_request['result'][d]['current_price']))) + str(
            data_request['result'][d]['current_price'])

        change_price = format(data_request['result'][d][f"price_change_percentage_{current_period}_in_currency"], '.2f')
        string_change_price = " " * (6 - len(str(change_price))) + str(change_price)

        text += f"<code>{string_number}|{string_slug}|{string_price}|{string_change_price}|</code>\n"

    return text
