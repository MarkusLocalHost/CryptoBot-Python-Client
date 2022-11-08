from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config


async def make_view_currency_after_find_request_keyboard(currencies, currency_name):
    view_currency_after_find_request_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        if currency['market_cap_rank'] > 1000:
            continue
        view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
            text=currency['name'],
            callback_data=currency['id']))

    view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
        text="Показать криптовалюты с меньшей капитализацией",
        callback_data=f"more_crypto-{currency_name}"))
    view_currency_after_find_request_keyboard.add(types.InlineKeyboardButton(
        text="Закрыть",
        callback_data="close"))

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
    view_currency_after_find_request_more_crypto = types.InlineKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        view_currency_after_find_request_more_crypto.add(types.InlineKeyboardButton(
            text=currency['name'],
            callback_data=currency['id']))

    view_currency_after_find_request_more_crypto.add(types.InlineKeyboardButton(
        text="Закрыть",
        callback_data="close"))

    return view_currency_after_find_request_more_crypto


async def make_view_action_after_receiving_short_info_keyboard(currency_name):
    view_action_after_receiving_short_info = InlineKeyboardMarkup(row_width=4,
                                                                  inline_keyboard=[
                                                                      [
                                                                          InlineKeyboardButton(
                                                                              text="Подробная информация",
                                                                              callback_data="view_detail_info"
                                                                          )
                                                                      ],
                                                                      [
                                                                          InlineKeyboardButton(
                                                                              text="Открыть в webapp",
                                                                              web_app=types.WebAppInfo(
                                                                                  url=f"{config.WEBHOOK_HOST}/currency/{currency_name}")
                                                                          )
                                                                      ],
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

    return view_action_after_receiving_short_info
