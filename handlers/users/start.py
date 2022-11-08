from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import I18N_DOMAIN, LOCALES_DIR
from keyboards.inline.start_keyboard import start_keyboard, select_language_keyboard
from loader import dp
from states.start_states import StartStates
from utils.misc.requests_type import make_request_get
from utils.token.token import generate_token

# get localization
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext


@dp.message_handler(CommandStart(), state="*")
async def select_language(message: types.Message, state: FSMContext):
    await message.answer(_("Выберите язык для продолжения"), reply_markup=select_language_keyboard)

    await StartStates.SelectLanguage.set()


@dp.callback_query_handler(state=StartStates.SelectLanguage)
async def start(call: types.CallbackQuery, state: FSMContext):
    data = {
        "telegramUserID": call.from_user.id,
        "language": call.data
    }
    token = await generate_token(data)
    endpoint = f"http://127.0.0.1:8080/api/account/new_account"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = await make_request_get(endpoint, headers)

    if r.json()['result'] == 'user in bd':
        await call.message.edit_text(_("Hello"), reply_markup=start_keyboard)
    else:
        await call.message.edit_text(_("Произошла ошибка"))

    await state.finish()
