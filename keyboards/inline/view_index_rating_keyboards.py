from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

view_type_of_index_rating_keyboard = InlineKeyboardMarkup(row_width=4,
                                                          inline_keyboard=[
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть в webapp формате",
                                                                      callback_data="view_webapp_type"
                                                                  )
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть в стандартном формате",
                                                                      callback_data="view_default_type"
                                                                  )
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Закрыть",
                                                                      callback_data="close_index_rating"
                                                                  )
                                                              ],
                                                          ])

view_type_of_index_rating_from_main_menu_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                         inline_keyboard=[
                                                                             [
                                                                                 InlineKeyboardButton(
                                                                                     text="Посмотреть в webapp формате",
                                                                                     callback_data="view_webapp_type"
                                                                                 )
                                                                             ],
                                                                             [
                                                                                 InlineKeyboardButton(
                                                                                     text="Посмотреть в стандартном "
                                                                                          "формате",
                                                                                     callback_data="view_default_type"
                                                                                 )
                                                                             ],
                                                                             [
                                                                                 InlineKeyboardButton(
                                                                                     text="Вернуться в меню",
                                                                                     callback_data="return_to_main_menu"
                                                                                 )
                                                                             ],
                                                                             [
                                                                                 InlineKeyboardButton(
                                                                                     text="Закрыть",
                                                                                     callback_data="close_index_rating"
                                                                                 )
                                                                             ],
                                                                         ])

view_web_app_link_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Просмотреть информацию",
                web_app=types.WebAppInfo(url=f"{config.WEBHOOK_HOST}/index_rating/data/?page=1")
            )
        ]
    ]
)


async def make_index_cb_keyboard(page):
    if page == 1:
        first_buttons = [
            InlineKeyboardButton(
                text="След. 10",
                callback_data="next"
            ),
        ]
    else:
        first_buttons = [
            InlineKeyboardButton(
                text="Пред. 10",
                callback_data="back"
            ),
            InlineKeyboardButton(
                text="След. 10",
                callback_data="next"
            ),
        ]

    index_cb_keyboard = InlineKeyboardMarkup(row_width=4,
                                             inline_keyboard=[
                                                 first_buttons,
                                                 [
                                                     InlineKeyboardButton(
                                                         text="USD",
                                                         callback_data="usd"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="RUB",
                                                         callback_data="rub"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="BTC",
                                                         callback_data="btc"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="ETH",
                                                         callback_data="eth"
                                                     ),
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text="24h",
                                                         callback_data="24h"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="7d",
                                                         callback_data="7d"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="30d",
                                                         callback_data="30d"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="1y",
                                                         callback_data="1y"
                                                     ),
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text="Закрыть",
                                                         callback_data="close_index_rating"
                                                     )
                                                 ]
                                             ])

    return index_cb_keyboard
