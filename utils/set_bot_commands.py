from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("menu", "Вывести главное меню"),
            types.BotCommand("find", "Найти криптовалюту"),
            types.BotCommand("index_rating", "Общая информация по цене"),
            types.BotCommand("view_trending", "Информация по трендам"),
            types.BotCommand("portfolio", "Мой портфель"),
            types.BotCommand("account", "Мой аккаунт"),
            types.BotCommand("new_observer", "Создать обсервер"),
            types.BotCommand("cancel_make_observer", "Отмена создания обсервера"),
            types.BotCommand("subscribe_change_price", "Подписаться на изменение цен")
        ]
    )
