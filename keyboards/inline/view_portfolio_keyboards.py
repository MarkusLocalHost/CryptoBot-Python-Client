from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

view_actions_without_currencies_in_portfolio_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                             inline_keyboard=[
                                                                                 [
                                                                                     InlineKeyboardButton(
                                                                                         text="Добавить криптовалюту в портфель",
                                                                                         callback_data="add_to_portfolio"
                                                                                     )
                                                                                 ],
                                                                                 [
                                                                                     InlineKeyboardButton(
                                                                                         text="Закрыть",
                                                                                         callback_data="cancel"
                                                                                     )
                                                                                 ],
                                                                             ])

view_actions_without_currencies_in_portfolio_from_main_menu_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                                            inline_keyboard=[
                                                                                                [
                                                                                                    InlineKeyboardButton(
                                                                                                        text="Добавить криптовалюту в портфель",
                                                                                                        callback_data="add_to_portfolio"
                                                                                                    )
                                                                                                ],
                                                                                                [
                                                                                                    InlineKeyboardButton(
                                                                                                        text="Вернуться в главное меню",
                                                                                                        callback_data="return_to_main_menu"
                                                                                                    )
                                                                                                ],
                                                                                                [
                                                                                                    InlineKeyboardButton(
                                                                                                        text="Закрыть",
                                                                                                        callback_data="cancel"
                                                                                                    )
                                                                                                ],
                                                                                            ])


async def make_view_currency_after_find_request_keyboard(currencies, currency_name):
    view_currency_after_find_request_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        if currency['market_cap_rank'] > 1000:
            continue
        view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
            text=currency['name'],
            callback_data=f"currency-{currency['symbol']}"))

    view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
        text="Показать криптовалюты с меньшей капитализацией",
        callback_data=f"more_crypto-{currency_name}"))
    view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_currency_after_find_request_keyboard


view_currency_after_find_request_no_results_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                            inline_keyboard=[
                                                                                [
                                                                                    InlineKeyboardButton(
                                                                                        text="Попробовать еще раз",
                                                                                        callback_data="another_try"
                                                                                    )
                                                                                ],
                                                                            ])


async def make_view_currency_after_find_request_more_crypto_keyboard(currencies):
    view_currency_after_find_request_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        if currency['market_cap_rank'] > 1000:
            continue
        view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
            text=currency['name'],
            callback_data=f"currency-{currency['symbol']}"))

    view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_currency_after_find_request_keyboard


view_actions_after_select_currency_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                   inline_keyboard=[
                                                                       [
                                                                           InlineKeyboardButton(
                                                                               text="Покупка",
                                                                               callback_data="buy"
                                                                           )
                                                                       ],
                                                                       [
                                                                           InlineKeyboardButton(
                                                                               text="Продажа",
                                                                               callback_data="sell"
                                                                           )
                                                                       ],
                                                                   ])

view_actions_after_fill_data_keyboard = InlineKeyboardMarkup(row_width=4,
                                                             inline_keyboard=[
                                                                 [
                                                                     InlineKeyboardButton(
                                                                         text="Подтвердить",
                                                                         callback_data="confirm"
                                                                     )
                                                                 ],
                                                                 [
                                                                     InlineKeyboardButton(
                                                                         text="Отмена",
                                                                         callback_data="cancel"
                                                                     )
                                                                 ],
                                                             ])


async def make_view_currencies_record_in_portfolio_keyboard(currencies, currency_name):
    text = f"Записи по {currency_name}\n\n"
    view_currencies_record_in_portfolio_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_currencies_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text=f"Добавить запись для {currency_name}",
        callback_data=f"add_record-{currency_name}"))

    for portfolio_record in currencies:
        if portfolio_record['cryptocurrency'] == currency_name:
            text += f"<code>Цена добавления: {portfolio_record['price']}</code>\n" \
                    f"<code>Тип:             {portfolio_record['type']}</code>\n" \
                    f"<code>Количество:      {portfolio_record['value']}</code>\n" \
                    f"<code>Дата:            {portfolio_record['createdAt']}</code>\n\n"

            view_currencies_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Перейти к записи {portfolio_record['createdAt']}",
                callback_data=f"record-{portfolio_record['id']}"))

    view_currencies_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_currencies_record_in_portfolio_keyboard, text


async def make_view_currency_record_in_portfolio_keyboard(currencies, currency_name):
    text = f"Запись с id {currency_name}\n\n"
    view_currency_record_in_portfolio_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)

    for portfolio_record in currencies:
        if portfolio_record['id'] == currency_name:
            text += f"<code>Цена добавления: {portfolio_record['price']}</code>\n" \
                    f"<code>Тип:             {portfolio_record['type']}</code>\n" \
                    f"<code>Количество:      {portfolio_record['value']}</code>\n" \
                    f"<code>Дата:            {portfolio_record['createdAt']}</code>\n\n"

            view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Изменить количество",
                callback_data=f"change_count_record-{portfolio_record['id']}"))
            view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Изменить цену",
                callback_data=f"change_price_record-{portfolio_record['id']}"))
            view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text=f"Удалить",
                callback_data=f"delete_record-{portfolio_record['id']}"))
            view_currency_record_in_portfolio_keyboard.add(types.InlineKeyboardButton(
                text="Назад",
                callback_data=f"back-{portfolio_record['cryptocurrency']}"))

    return view_currency_record_in_portfolio_keyboard, text


async def make_delete_confirmation_keyboard(currency_name):
    delete_confirmation_keyboard = InlineKeyboardMarkup(row_width=4,
                                                        inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(
                                                                    text="Подтвердить",
                                                                    callback_data="confirm_delete"
                                                                )
                                                            ],
                                                            [
                                                                InlineKeyboardButton(
                                                                    text="Отменить",
                                                                    callback_data=f"cancel_delete-{currency_name}"
                                                                )
                                                            ],
                                                        ])

    return delete_confirmation_keyboard
