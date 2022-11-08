from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data.config import I18N_DOMAIN, LOCALES_DIR
from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
