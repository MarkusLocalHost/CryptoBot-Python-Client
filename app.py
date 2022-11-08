import logging
import os
import pickle

import aiohttp_jinja2
import aioredis
import jinja2
import requests

from data import config
from loader import dp, bot
from aiohttp import web

from middlewares.language import setup_middleware
from utils.load_users_languages import load_users_languages
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from web_app import routes as webapp_routes


async def on_startup(dispatcher):
    await bot.set_webhook(
        url=config.WEBHOOK_URL
    )

    import middlewares
    import filters

    setup_middleware(dispatcher)

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Загружает языки пользователей
    await load_users_languages()

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    data = await bot.get_webhook_info()

    await bot.delete_webhook()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    app = web.Application()
    app["bot"] = bot
    app.add_routes(webapp_routes)
    app.router.add_static(prefix='/static', path='static')

    # executor.start_polling(dp, on_startup=on_startup)

    executor.set_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        web_app=app,
    )

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(os.path.join(os.path.join(os.getcwd(), "static"))))
    web.run_app(app, port=config.WEBAPP_PORT, host=config.WEBAPP_HOST)
