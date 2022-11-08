from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

view_actions_in_create_price_observer = InlineKeyboardMarkup(row_width=4,
                                                             inline_keyboard=[
                                                                 [
                                                                     InlineKeyboardButton(
                                                                         text="Вернуться в главное меню",
                                                                         callback_data="return_to_main_menu"
                                                                     )
                                                                 ]
                                                             ])

view_actions_after_create_price_observer = InlineKeyboardMarkup(row_width=4,
                                                                inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text="Вернуться в главное меню",
                                                                            callback_data="return_to_main_menu"
                                                                        )
                                                                    ]
                                                                ])


async def make_view_actions_in_search_currency_for_observer_keyboard(currency_name):
    view_actions_in_search_currency_for_observer = InlineKeyboardMarkup(row_width=4,
                                                                        inline_keyboard=[
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Просмотреть информацию в webapp",
                                                                                    web_app=types.WebAppInfo(
                                                                                        url=f"{config.WEBHOOK_HOST}/try_find/{currency_name}")
                                                                                )
                                                                            ],
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Просмотреть информацию в стандартном виде",
                                                                                    callback_data="view_currency_standard_view"
                                                                                )
                                                                            ],
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Вернуться в главное меню",
                                                                                    callback_data="return_to_main_menu"
                                                                                )
                                                                            ]
                                                                        ])

    return view_actions_in_search_currency_for_observer


async def make_view_currency_after_find_request_keyboard(currencies):
    view_currency_after_find_request_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)

    for currency in currencies:
        view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
            text=currency['name'],
            callback_data=currency['name']))

    return view_currency_after_find_request_keyboard


view_action_after_receiving_short_info = InlineKeyboardMarkup(row_width=4,
                                                              inline_keyboard=[
                                                                  [
                                                                      InlineKeyboardButton(
                                                                          text="Создать обсервер",
                                                                          callback_data="make_observer"
                                                                      )
                                                                  ],
                                                                  [
                                                                      InlineKeyboardButton(
                                                                          text="Отмена",
                                                                          callback_data="cancel_make_observer"
                                                                      )
                                                                  ]
                                                              ])


async def make_view_supported_vs_currencies_after_receiving_keyboard(currencies):
    view_supported_vs_currencies_after_receiving = types.InlineKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        view_supported_vs_currencies_after_receiving.add(types.InlineKeyboardButton(
            text=f"{currency}",
            callback_data=f"{currency}"))
    view_supported_vs_currencies_after_receiving.add(types.InlineKeyboardButton(
        text="Отмена",
        callback_data="cancel_make_observer"))

    return view_supported_vs_currencies_after_receiving


view_action_after_receiving_observer_info = InlineKeyboardMarkup(row_width=4,
                                                                 inline_keyboard=[
                                                                     [
                                                                         InlineKeyboardButton(
                                                                             text="Создать обсервер",
                                                                             callback_data="finish_make_observer"
                                                                         )
                                                                     ],
                                                                     [
                                                                         InlineKeyboardButton(
                                                                             text="Отмена",
                                                                             callback_data="cancel_make_observer"
                                                                         )
                                                                     ]
                                                                 ])
