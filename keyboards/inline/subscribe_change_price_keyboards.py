from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subscribe_change_price_keyboard = InlineKeyboardMarkup(row_width=4,
                                                       inline_keyboard=[
                                                           [
                                                               InlineKeyboardButton(
                                                                   text="Выбрать настройки",
                                                                   callback_data="settings"
                                                               )
                                                           ],
                                                           [
                                                               InlineKeyboardButton(
                                                                   text="Закрыть",
                                                                   callback_data="cancel_subscribe"
                                                               )
                                                           ],
                                                       ])

subscribe_change_price_from_main_menu_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                      inline_keyboard=[
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Выбрать настройки",
                                                                                  callback_data="settings"
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
                                                                                  callback_data="cancel_subscribe"
                                                                              )
                                                                          ],
                                                                      ])


async def make_subscribe_change_price_settings_keyboard(min_20_is_active, min_60_is_active):
    if min_20_is_active:
        min_20_is_active_button = [
            InlineKeyboardButton(
                text="✅ Отслеживать скачки на 20 минут",
                callback_data="deactivate_20_minutes"
            ),
        ]
    else:
        min_20_is_active_button = [
            InlineKeyboardButton(
                text="❌ Отслеживать скачки на 20 минут",
                callback_data="activate_20_minutes"
            ),
        ]

    if min_60_is_active:
        min_60_is_active_button = [
            InlineKeyboardButton(
                text="✅ Отслеживать скачки на 60 минут",
                callback_data="deactivate_60_minutes"
            ),
        ]
    else:
        min_60_is_active_button = [
            InlineKeyboardButton(
                text="❌ Отслеживать скачки на 60 минут",
                callback_data="activate_60_minutes"
            ),
        ]

    if min_20_is_active or min_60_is_active:
        subscribe_change_price_settings_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                        inline_keyboard=[
                                                                            min_20_is_active_button,
                                                                            min_60_is_active_button,
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Дальше",
                                                                                    callback_data="next_settings"
                                                                                ),
                                                                            ],
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Закрыть",
                                                                                    callback_data="close_settings"
                                                                                )
                                                                            ]
                                                                        ])
    else:
        subscribe_change_price_settings_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                        inline_keyboard=[
                                                                            min_20_is_active_button,
                                                                            min_60_is_active_button,
                                                                            [
                                                                                InlineKeyboardButton(
                                                                                    text="Закрыть",
                                                                                    callback_data="close_settings"
                                                                                )
                                                                            ]
                                                                        ])

    return subscribe_change_price_settings_keyboard


change_next_settings_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                      inline_keyboard=[
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Отправлять все результаты",
                                                                                  callback_data="finish"
                                                                              )
                                                                          ],
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Отправлять если процент изменения больше x",
                                                                                  callback_data="percent_bigger"
                                                                              )
                                                                          ],
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Отправлять если процент изменения меньше x",
                                                                                  callback_data="percent_smaller"
                                                                              )
                                                                          ],
[
                                                                              InlineKeyboardButton(
                                                                                  text="Назад",
                                                                                  callback_data="back_settings"
                                                                              )
                                                                          ],
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Закрыть",
                                                                                  callback_data="cancel_subscribe"
                                                                              )
                                                                          ],
                                                                      ])


async def make_set_next_action_after_first_filter_keyboard(filter_type):
    set_next_action_after_first_filter_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    set_next_action_after_first_filter_keyboard.add(types.InlineKeyboardButton(
        text="Закончить создание",
        callback_data="finish"))
    if filter_type == "percent_smaller":
        set_next_action_after_first_filter_keyboard.add(types.InlineKeyboardButton(
            text="Отправлять если процент изменения больше x",
            callback_data="percent_bigger"))
    elif filter_type == "percent_bigger":
        set_next_action_after_first_filter_keyboard.add(types.InlineKeyboardButton(
            text="Отправлять если процент изменения не больше x",
            callback_data="percent_smaller"))
    set_next_action_after_first_filter_keyboard.add(types.InlineKeyboardButton(
        text="Закрыть",
        callback_data="close_settings"))

    return set_next_action_after_first_filter_keyboard


set_next_action_after_second_filter_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                      inline_keyboard=[
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Закончить создание",
                                                                                  callback_data="finish"
                                                                              )
                                                                          ],
                                                                          [
                                                                              InlineKeyboardButton(
                                                                                  text="Закрыть",
                                                                                  callback_data="close_settings"
                                                                              )
                                                                          ],
                                                                      ])

view_action_after_create_percentage_observer = InlineKeyboardMarkup(row_width=4,
                                                                inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text="Вернуться в главное меню",
                                                                            callback_data="return_to_main_menu"
                                                                        )
                                                                    ]
                                                                ])
