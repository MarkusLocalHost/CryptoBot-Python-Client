from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_language_keyboard = InlineKeyboardMarkup(row_width=4,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(
                                                            text="Русский",
                                                            callback_data="ru"
                                                        ),
                                                        InlineKeyboardButton(
                                                            text="Український",
                                                            callback_data="uk"
                                                        ),
                                                    ],
                                                    [
                                                        InlineKeyboardButton(
                                                            text="English",
                                                            callback_data="en"
                                                        ),
                                                    ]
                                                ])

start_keyboard = InlineKeyboardMarkup(row_width=4,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(
                                                  text="Мой аккаунт",
                                                  callback_data="my_account_from_start_menu"
                                              ),
                                              InlineKeyboardButton(
                                                  text="Моё портфолио",
                                                  callback_data="my_portfolio_from_start_menu"
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Создать обсервер на цены",
                                                  callback_data="create_price_observer_from_start_menu"
                                              ),
                                              InlineKeyboardButton(
                                                  text="Создать обсервер на проценты",
                                                  callback_data="create_percent_observer_from_start_menu"
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Посмотреть индекс цены",
                                                  callback_data="view_index_rating_from_start_menu"
                                              )
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Подобрать обмен с bestchange",
                                                  callback_data="view_exchange_rate_from_bestchange_from_start_menu"
                                              )
                                          ]
                                      ])
