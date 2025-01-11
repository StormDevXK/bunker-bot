from os import getenv
from os.path import exists
import asyncio
import datetime

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select


# Загрузка переменных окружения из файла .env, если он существует
if exists(".env"):
    load_dotenv()


# Инициализация SQLAlchemy для работы с базой данных
users_engine = create_async_engine("sqlite+aiosqlite:///users.db", echo=True)
Base = declarative_base()
# noinspection PyTypeChecker
async_session_maker = sessionmaker(
    bind=users_engine,  # Явное указание привязки к движку
    class_=AsyncSession,  # Класс для асинхронных сессий
    expire_on_commit=False
)


# Определение модели пользователя
class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now)


# Создание таблиц при первом запуске
async def init_db():
    async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Чтение токен бота из переменной окружения
BOT_TOKEN: str = getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверьте файл .env или переменные окружения.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# noinspection PyTypeChecker
@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Добро пожаловать в бункер!\nЧтобы начать играть нужно создать лобби \
- /create\nИли подключится к уже созданному - /join <ID>\nЕсли возникнут вопросы - /help")

    # Работа с асинхронной сессией
    async with async_session_maker() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if not existing_user:
            new_user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code
            )
            session.add(new_user)
            await session.commit()


@dp.message(Command('help'))
async def helps(message: types.Message):
    await bot.send_message(message.chat.id, "Список всех доступных комманд:\n/create - Создать игру.\n/join <ID> \
- Подключится к существующей игре.\n/exit - Выйти из игры.")


async def main():
    await init_db()  # Инициализация базы данных
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
