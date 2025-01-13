from aiogram import types, Bot
from database import save_user_data_to_db, create_lobby, join_lobby, exit_lobby


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


# Оработчик команды /create
async def create_handler(message: types.Message, bot: Bot):

    # Создание lobby и получение его id
    lobby_id = await create_lobby(message.from_user.id)

    await bot.send_message(
        message.chat.id, f"Вы создали лобби с айди {lobby_id}\n"
        "Поделитесь им чтобы другие игроки смогли подключиться к вам."
    )


# Оработчик команды /join
async def join_handler(message: types.Message, bot: Bot):

    try:
        lobby_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Пожалуйста, укажите ID игры в формате /join <ID>.")
        return

    # Подключение к lobby по id
    try:
        await join_lobby(message.from_user.id, lobby_id)
    except ():
        await message.reply("Пожалуйста, перепроверте ваш <ID>")
        return

    await bot.send_message(message.chat.id, f"Вы присоединились к лобби с айди {lobby_id}")


# Оработчик команды /exit
async def exit_handler(message: types.Message, bot: Bot):

    # Выход из лобби
    try:
        await exit_lobby(message.from_user.id)
    except ():
        await message.reply("Вы не находитесь в лобби")
        return

    await bot.send_message(message.chat.id, f"Вы вышли из лобби.")
