import logging
import pickle

import aioredis

from data import config
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token


async def load_users_languages():
    data = {}
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/info/users_languages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result']:
        redis = await aioredis.create_redis_pool(config.REDIS_IP)
        await redis.set(f"data_bd-users_languages", pickle.dumps(r.json()['result']))
        redis.close()
        await redis.wait_closed()

        logging.info("BD is loaded")
    else:
        logging.exception("bd is not loaded")
