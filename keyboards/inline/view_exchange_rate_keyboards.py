from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

view_type_exchange_type = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Российские банки",
                                                           callback_data="view_banks"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Электронные кошельки",
                                                           callback_data="view_wallets"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Посмотреть криптовалюты",
                                                           callback_data="view_cryptos"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Вернуться в меню",
                                                           callback_data="return_to_main_menu"
                                                       )
                                                   ]
                                               ])

view_type_exchange_type_only_bank_and_wallet = InlineKeyboardMarkup(row_width=1,
                                                                    inline_keyboard=[
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Российские банки",
                                                                                callback_data="view_banks"
                                                                            )
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Электронные кошельки",
                                                                                callback_data="view_wallets"
                                                                            )
                                                                        ]
                                                                    ])

view_type_exchange_type_only_crypto = InlineKeyboardMarkup(row_width=1,
                                                           inline_keyboard=[
                                                               [
                                                                   InlineKeyboardButton(
                                                                       text="Посмотреть криптовалюты",
                                                                       callback_data="view_cryptos"
                                                                   )
                                                               ]
                                                           ])


async def make_view_banks_keyboard(banks):
    if "42;" in banks:
        sberbank = InlineKeyboardButton(
            text="✅ Сбербанк",
            callback_data="42;"
        )
    else:
        sberbank = InlineKeyboardButton(
            text="Сбербанк",
            callback_data="42;"
        )

    if "51;" in banks:
        vtb = InlineKeyboardButton(
            text="✅ ВТБ",
            callback_data="51;"
        )
    else:
        vtb = InlineKeyboardButton(
            text="ВТБ",
            callback_data="51;"
        )

    if "52;" in banks:
        alfaclick = InlineKeyboardButton(
            text="✅ Альфабанк",
            callback_data="52;"
        )
    else:
        alfaclick = InlineKeyboardButton(
            text="Альфабанк",
            callback_data="52;"
        )

    if "105;" in banks:
        tinkoff = InlineKeyboardButton(
            text="✅ Тинькофф",
            callback_data="105;"
        )
    else:
        tinkoff = InlineKeyboardButton(
            text="Тинькофф",
            callback_data="105;"
        )

    if "64;" in banks:
        russtandart = InlineKeyboardButton(
            text="✅ Русский стандарт",
            callback_data="64;"
        )
    else:
        russtandart = InlineKeyboardButton(
            text="Русский стандарт",
            callback_data="64;"
        )

    if "79;" in banks:
        avangard = InlineKeyboardButton(
            text="✅ Авангард",
            callback_data="79;"
        )
    else:
        avangard = InlineKeyboardButton(
            text="Авангард",
            callback_data="79;"
        )

    if "53;" in banks:
        psbank = InlineKeyboardButton(
            text="✅ Промсвязьбанк",
            callback_data="53;"
        )
    else:
        psbank = InlineKeyboardButton(
            text="Промсвязьбанк",
            callback_data="53;"
        )

    if "95;" in banks:
        gazprombank = InlineKeyboardButton(
            text="✅ Газпромбанк",
            callback_data="95;"
        )
    else:
        gazprombank = InlineKeyboardButton(
            text="Газпромбанк",
            callback_data="95;"
        )

    if "157;" in banks:
        raiffeisen = InlineKeyboardButton(
            text="✅ Райффазенбанк",
            callback_data="157;"
        )
    else:
        raiffeisen = InlineKeyboardButton(
            text="Райффазенбанк",
            callback_data="157;"
        )

    if "176;" in banks:
        openbank = InlineKeyboardButton(
            text="✅ Открытие",
            callback_data="176;"
        )
    else:
        openbank = InlineKeyboardButton(
            text="Открытие",
            callback_data="176;"
        )

    if banks == "":
        next = ""
    else:
        next = [
            InlineKeyboardButton(
                text="Подтвердить",
                callback_data="confirm"
            )
        ]

    view_banks_with_multiple_value = InlineKeyboardMarkup(row_width=3,
                                                          inline_keyboard=[
                                                              [
                                                                  sberbank,
                                                                  vtb,
                                                                  alfaclick
                                                              ],
                                                              [
                                                                  tinkoff,
                                                                  russtandart,
                                                                  avangard
                                                              ],
                                                              [
                                                                  psbank,
                                                                  gazprombank,
                                                                  raiffeisen
                                                              ],
                                                              [
                                                                  openbank
                                                              ],
                                                              next,
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Назад",
                                                                      callback_data="back"
                                                                  )
                                                              ]
                                                          ])

    return view_banks_with_multiple_value


view_banks = InlineKeyboardMarkup(row_width=3,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text="Сбербанк",
                                              callback_data="42;"
                                          ),
                                          InlineKeyboardButton(
                                              text="ВТБ",
                                              callback_data="51;"
                                          ),
                                          InlineKeyboardButton(
                                              text="Альфабанк",
                                              callback_data="52;"
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="Тинькофф",
                                              callback_data="105;"
                                          ),
                                          InlineKeyboardButton(
                                              text="Русский стандарт",
                                              callback_data="64;"
                                          ),
                                          InlineKeyboardButton(
                                              text="Авангард",
                                              callback_data="79;"
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="Промсвязьбанк",
                                              callback_data="53;"
                                          ),
                                          InlineKeyboardButton(
                                              text="Газпромбанк",
                                              callback_data="95;"
                                          ),
                                          InlineKeyboardButton(
                                              text="Райффазенбанк",
                                              callback_data="157;"
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="Открытие",
                                              callback_data="176;"
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text="Назад",
                                              callback_data="back"
                                          )
                                      ]
                                  ])


async def make_view_wallets_keyboard(wallets):
    if "6;" in wallets:
        yoomoney = InlineKeyboardButton(
            text="✅ YooMoney",
            callback_data="6;"
        )
    else:
        yoomoney = InlineKeyboardButton(
            text="YooMoney",
            callback_data="6;"
        )

    if "63;" in wallets:
        qiwi = InlineKeyboardButton(
            text="✅ QIWI",
            callback_data="63;"
        )
    else:
        qiwi = InlineKeyboardButton(
            text="QIWI",
            callback_data="63;"
        )

    view_wallets_with_multiple_value = InlineKeyboardMarkup(row_width=1,
                                                            inline_keyboard=[
                                                                [
                                                                    yoomoney
                                                                ],
                                                                [
                                                                    qiwi
                                                                ],
                                                                [
                                                                    InlineKeyboardButton(
                                                                        text="Подтвердить",
                                                                        callback_data="confirm"
                                                                    )
                                                                ],
                                                                [
                                                                    InlineKeyboardButton(
                                                                        text="Назад",
                                                                        callback_data="back"
                                                                    )
                                                                ]
                                                            ])

    return view_wallets_with_multiple_value


view_wallets = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="YooMoney",
                                                callback_data="6;"
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="QIWI",
                                                callback_data="63;"
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Назад",
                                                callback_data="back"
                                            )
                                        ]
                                    ])

view_cryptos = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text="Bitcoin",
                                                callback_data="93"
                                            ),
                                            InlineKeyboardButton(
                                                text="Ethereum",
                                                callback_data="139"
                                            ),
                                            InlineKeyboardButton(
                                                text="Litecoin",
                                                callback_data="99"
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Ripple",
                                                callback_data="161"
                                            ),
                                            InlineKeyboardButton(
                                                text="Monero",
                                                callback_data="149"
                                            ),
                                            InlineKeyboardButton(
                                                text="Dogecoin",
                                                callback_data="115"
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Polygon",
                                                callback_data="138"
                                            ),
                                            InlineKeyboardButton(
                                                text="Dash",
                                                callback_data="140"
                                            ),
                                            InlineKeyboardButton(
                                                text="Zcash",
                                                callback_data="162"
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="Назад",
                                                callback_data="back"
                                            )
                                        ]
                                    ])
