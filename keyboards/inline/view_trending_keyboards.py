from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

view_source_for_trending_currencies_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                    inline_keyboard=[
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinGecko Trending",
                                                                                callback_data="coingecko_trending")
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinMarketCap Trending",
                                                                                callback_data="coinmarketcap_trending")
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinMarketCap Gainers",
                                                                                callback_data="coinmarketcap_gainers"),
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinMarketCap Losers",
                                                                                callback_data="coinmarketcap_losers"),
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinMarketCap Most Visited",
                                                                                callback_data="coinmarketcap_most_visited"),
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="CoinMarketCap Recently Added",
                                                                                callback_data="coinmarketcap_recently_added"),
                                                                        ],
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text="Закрыть это меню",
                                                                                callback_data="close_trending"),
                                                                        ],
                                                                    ])


async def make_view_action_after_receiving_short_info_keyboard(currency_name):
    view_action_after_receiving_short_info_keyboard = InlineKeyboardMarkup(row_width=4,
                                                                           inline_keyboard=[
                                                                               [
                                                                                   InlineKeyboardButton(
                                                                                       text="Посмотреть подробную информацию",
                                                                                       callback_data="view_detail_info")
                                                                               ],
                                                                               [
                                                                                   InlineKeyboardButton(
                                                                                       text="Добавить в портфель",
                                                                                       callback_data=f"add_to_portfolio-{currency_name}")
                                                                               ],
                                                                               [
                                                                                   InlineKeyboardButton(
                                                                                       text="Создать обсервер",
                                                                                       callback_data="make_observer"),
                                                                               ],
                                                                               [
                                                                                   InlineKeyboardButton(
                                                                                       text="Назад",
                                                                                       callback_data="back"),
                                                                               ],
                                                                           ])

    return view_action_after_receiving_short_info_keyboard
