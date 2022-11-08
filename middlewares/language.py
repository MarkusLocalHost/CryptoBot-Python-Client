import logging
import pickle

import aioredis
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data import config
from data.config import I18N_DOMAIN, LOCALES_DIR


async def get_lang(user_id):
    redis = await aioredis.create_redis_pool(config.REDIS_IP)
    data_bd = await redis.get(f"data_bd-users_languages")
    if data_bd is not None:
        data_bd = pickle.loads(data_bd)
    redis.close()
    await redis.wait_closed()

    if data_bd is not None:
        return data_bd.get(f"{user_id}")
    else:
        return "ru"


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        user = types.User.get_current()

        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
