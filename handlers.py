from aiogram import types, Bot
from database import save_user_data_to_db


# Обработчик команды /start
async def start_handler(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id, "Добро пожаловать в бункер!\n"
        "Чтобы начать играть нужно создать лобби - /create\n"
        "Или подключиться к уже созданному - /join <ID>\n"
        "Если возникнут вопросы - /help"
    )

    # Работа с базой данных
    await save_user_data_to_db(message)


# Обработчик команды /help
async def help_handler(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id, "Список всех доступных команд:\n"
        "/create - Создать игру.\n"
        "/join <ID> - Подключиться к существующей игре.\n"
        "/exit - Выйти из игры."
    )
