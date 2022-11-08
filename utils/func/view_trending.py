from aiogram import types

from states.view_trending_states import ViewTrendingStates


async def make_message_by_data_request(r, call):
    if r.json()['result'] is not None:
        view_trending_currency_after_find_request_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        for currency in r.json()['result']:
            view_trending_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
                text=f"{currency['name']} - {currency['symbol']}",
                callback_data=currency['symbol']))

        view_trending_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back"))

        await call.message.edit_text("Выберите интересующую вас криптовалюту для более подробного просмотра",
                                     reply_markup=view_trending_currency_after_find_request_keyboard)

        await ViewTrendingStates.SendNameOfTrendingCurrency.set()
    else:
        # обработать
        await call.message.edit_text("Data не найдена")