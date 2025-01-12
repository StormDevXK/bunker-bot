from aiogram import types, Bot
from aiogram.filters import Command
from sqlalchemy.future import select
from database import UserData, async_session_maker


# Обработчик команды /start
async def start_handler(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id, "Добро пожаловать в бункер!\n"
        "Чтобы начать играть нужно создать лобби - /create\n"
        "Или подключиться к уже созданному - /join <ID>\n"
        "Если возникнут вопросы - /help"
    )

    # Работа с базой данных
    async with async_session_maker() as session:
        query = select(UserData).where(UserData.user_id == message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if not existing_user:
            new_user_data = UserData(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code
            )
            session.add(new_user_data)
            await session.commit()


# Обработчик команды /help
async def help_handler(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id, "Список всех доступных команд:\n"
        "/create - Создать игру.\n"
        "/join <ID> - Подключиться к существующей игре.\n"
        "/exit - Выйти из игры."
    )
