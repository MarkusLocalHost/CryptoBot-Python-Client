import math

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dateutil.parser import parse


async def make_action_in_account_keyboard(return_to_main_menu):
    if return_to_main_menu:
        action_in_account_keyboard = InlineKeyboardMarkup(row_width=4,
                                                          inline_keyboard=[
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мои обсервера",
                                                                      callback_data="view_my_observers"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мои обсервера на проценты",
                                                                      callback_data="view_my_percentage_observers"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мой портфель",
                                                                      callback_data="view_my_portfolio"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Подписка и лимиты",
                                                                      callback_data="view_my_subscription"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Вернуться в главное меню",
                                                                      callback_data="return_to_main_menu")
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Закрыть это меню",
                                                                      callback_data="close_account"),
                                                              ]
                                                          ])
    else:
        action_in_account_keyboard = InlineKeyboardMarkup(row_width=4,
                                                          inline_keyboard=[
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мои обсервера",
                                                                      callback_data="view_my_observers"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мои обсервера на проценты",
                                                                      callback_data="view_my_percentage_observers"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Посмотреть мой портфель",
                                                                      callback_data="view_my_portfolio"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Подписка и лимиты",
                                                                      callback_data="view_my_subscription"),
                                                              ],
                                                              [
                                                                  InlineKeyboardButton(
                                                                      text="Закрыть это меню",
                                                                      callback_data="close_account"),
                                                              ]
                                                          ])

    return action_in_account_keyboard


async def make_view_action_after_receiving_observers_keyboard(observers, page):
    view_action_after_receiving_observers = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_action_after_receiving_observers.add(types.InlineKeyboardButton(
        text="Создать обсервер",
        callback_data="create_observer"))

    text = ""
    num = 0
    end_page = math.ceil(len(observers) // 5)

    for observer in observers:
        if 5 * (page - 1) <= num < 5 * page:
            view_action_after_receiving_observers.add(types.InlineKeyboardButton(
                text=f"{observer['cryptoSymbol']} в {observer['currencyOfValue']} на {observer['expectedValue']}",
                callback_data=f"observer_{observer['id']}"))

        if observer['isActive'] == True:
            sign = "✅"
        else:
            sign = "🛑"

        text += f"Обсервер №{num + 1}\n" \
                f"Статус: {sign}\n\n"
        num += 1

    if end_page > 1:
        if page == 1:
            view_action_after_receiving_observers.row(
                types.InlineKeyboardButton(text=f"{page}", callback_data="page"),
                types.InlineKeyboardButton(text=">", callback_data="next"),
            )
        elif page == end_page:
            view_action_after_receiving_observers.row(
                types.InlineKeyboardButton(text="<", callback_data="prev"),
                types.InlineKeyboardButton(text=f"{page}", callback_data="page"),
            )
        else:
            view_action_after_receiving_observers.row(
                types.InlineKeyboardButton(text="<", callback_data="prev"),
                types.InlineKeyboardButton(text=f"{page}", callback_data="page"),
                types.InlineKeyboardButton(text=">", callback_data="next"),
            )

    view_action_after_receiving_observers.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_action_after_receiving_observers, text


async def make_view_action_after_receiving_current_observer_keyboard(observers, call, state):
    view_action_after_receiving_current_observer = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_action_after_receiving_current_observer.add(types.InlineKeyboardButton(
        text="Удалить",
        callback_data="delete"))

    text = ""
    for observer in observers:
        if observer['id'] == call.data.replace("observer_", ""):
            if observer['isActive']:
                status = "Активен"

                view_action_after_receiving_current_observer.add(types.InlineKeyboardButton(
                    text="Сделать неактивным",
                    callback_data="deactivate"))
            else:
                status = "Не активен"

                view_action_after_receiving_current_observer.add(types.InlineKeyboardButton(
                    text="Сделать активным",
                    callback_data="activate"))

            time = parse(observer['createdAt'])
            text = f"<code>" \
                   f"Криптовалюта: {observer['cryptoName']}\n" \
                   f"Значение:     {observer['expectedValue']} {observer['currencyOfValue']}\n" \
                   f"Tier:         {observer['tier']}\n" \
                   f"Статус:       {status}\n" \
                   f"Создан:       {time.date()} {time.time().hour}:{time.time().minute}" \
                   f"</code>"

            async with state.proxy() as data:
                data['selected_observer'] = call.data.replace("observer_", "")
        else:
            continue

    view_action_after_receiving_current_observer.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_action_after_receiving_current_observer, text


async def make_view_action_after_receiving_percentage_observers(observers, call, state):
    view_action_after_receiving_percentage_observers = types.InlineKeyboardMarkup(resize_keyboard=True)

    text = ""
    textTerm = ""
    num = 0
    for percent_observer in observers:
        view_action_after_receiving_percentage_observers.add(types.InlineKeyboardButton(
            text=f"Обсервер №{num + 1}",
            callback_data=f"{percent_observer['id']}"))

        if percent_observer['observe_20_minutes']:
            sign20Minutes = "✅"
        else:
            sign20Minutes = "❌"

        if percent_observer['observe_60_minutes']:
            sign60Minutes = "✅"
        else:
            sign60Minutes = "❌"

        if percent_observer['first_filter_type'] == "" and percent_observer['second_filter_type'] == "":
            textTerm = "нет"
        elif percent_observer['first_filter_type'] == "percent_bigger" and percent_observer['second_filter_type'] == "":
            textTerm = f">{percent_observer['first_filter_amount']}%"
        elif percent_observer['first_filter_type'] == "percent_smaller" and percent_observer[
            'second_filter_type'] == "":
            textTerm = f"<{percent_observer['first_filter_amount']}%"
        elif percent_observer['first_filter_type'] == "percent_bigger" and percent_observer[
            'second_filter_type'] == "percent_smaller":
            textTerm = f">{percent_observer['first_filter_amount']}% и <{percent_observer['second_filter_amount']}%"
        elif percent_observer['first_filter_type'] == "percent_smaller" and percent_observer[
            'second_filter_type'] == "percent_bigger":
            textTerm = f">{percent_observer['second_filter_amount']}% и <{percent_observer['first_filter_amount']}%"

        text += f"Обсервер №{num + 1}\n" \
                f"Каждые 20 минут {sign20Minutes}\n" \
                f"Каждые 60 минут {sign60Minutes}\n" \
                f"Условия: {textTerm}" \
                f"\n"
        num += 1

    view_action_after_receiving_percentage_observers.add(types.InlineKeyboardButton(
        text="Создать обсервер",
        callback_data="create_percent_observer_from_account"))
    view_action_after_receiving_percentage_observers.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_action_after_receiving_percentage_observers, text


async def make_view_action_after_receiving_current_percentage_observer(observers, call, state):
    view_action_after_receiving_current_percentage_observer = types.InlineKeyboardMarkup(resize_keyboard=True)
    view_action_after_receiving_current_percentage_observer.add(types.InlineKeyboardButton(
        text="Удалить",
        callback_data="delete"))

    text = ""
    textTerm = ""
    for observer in observers:
        if observer['id'] == call.data:
            if observer['observe_20_minutes']:
                sign20Minutes = "✅"
            else:
                sign20Minutes = "❌"

            if observer['observe_60_minutes']:
                sign60Minutes = "✅"
            else:
                sign60Minutes = "❌"

            if observer['first_filter_type'] == "" and observer['second_filter_type'] == "":
                textTerm = "нет"
            elif observer['first_filter_type'] == "percent_bigger" and observer[
                'second_filter_type'] == "":
                textTerm = f">{observer['first_filter_amount']}%"
            elif observer['first_filter_type'] == "percent_smaller" and observer[
                'second_filter_type'] == "":
                textTerm = f"<{observer['first_filter_amount']}%"
            elif observer['first_filter_type'] == "percent_bigger" and observer[
                'second_filter_type'] == "percent_smaller":
                textTerm = f">{observer['first_filter_amount']}% и <{observer['second_filter_amount']}%"
            elif observer['first_filter_type'] == "percent_smaller" and observer[
                'second_filter_type'] == "percent_bigger":
                textTerm = f">{observer['second_filter_amount']}% и <{observer['first_filter_amount']}%"

            time = parse(observer['createdAt'])
            text += f"Каждые 20 минут {sign20Minutes}\n" \
                    f"Каждые 60 минут {sign60Minutes}\n" \
                    f"Условия: {textTerm}\n" \
                    f"Создан: {time.date()} {time.time().hour}:{time.time().minute}"
            async with state.proxy() as data:
                data['selected_percentage_observer'] = call.data
        else:
            continue

    view_action_after_receiving_current_percentage_observer.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back"))

    return view_action_after_receiving_current_percentage_observer, text


view_action_after_delete_observer_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                  inline_keyboard=[
                                                                      [
                                                                          InlineKeyboardButton(
                                                                              text="Вернуться к обсерверам",
                                                                              callback_data="return_to_observers"
                                                                          )
                                                                      ],
                                                                      [
                                                                          InlineKeyboardButton(
                                                                              text="Закрыть",
                                                                              callback_data="close_account"
                                                                          )
                                                                      ],
                                                                  ])

view_action_after_view_subscription_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                    inline_keyboard=[
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Ввести промокод",
                                                                                callback_data="promocode"
                                                                            )
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Оплатить подписку",
                                                                                callback_data="make_payment"
                                                                            )
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Назад",
                                                                                callback_data="back"
                                                                            )
                                                                        ],
                                                                    ])

view_action_in_enter_promo_code_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text="Назад",
                                                                            callback_data="back"
                                                                        )
                                                                    ],
                                                                ])

view_action_after_enter_promo_code_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                   inline_keyboard=[
                                                                       [
                                                                           InlineKeyboardButton(
                                                                               text="Попробовать еще раз",
                                                                               callback_data="retry_promo_code"
                                                                           )
                                                                       ],
                                                                       [
                                                                           InlineKeyboardButton(
                                                                               text="Назад",
                                                                               callback_data="back"
                                                                           )
                                                                       ],
                                                                   ])
