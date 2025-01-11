from os import getenv
from os.path import exists
import asyncio
import datetime

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


# Загрузка переменных окружения из файла .env, если он существует
if exists(".env"):
    load_dotenv()


# Инициализация SQLAlchemy для работы с базой данных
users_engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Session = sessionmaker(bind=users_engine)
session = Session()


# Определение модели пользователя
class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now)


# Создание таблиц, если они еще не существуют
Base.metadata.create_all(users_engine)


# Чтение токен бота из переменной окружения
BOT_TOKEN: str = getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверьте файл .env или переменные окружения.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Добро пожаловать в бункер!\nЧтобы начать играть нужно создать лобби \
- /create\nИли подключится к уже созданному - /join <ID>\nЕсли возникнут вопросы - /help")

    # Проверка на наличие пользователя в базе
    existing_user = session.query(User).filter_by(user_id=message.from_user.id).first()
    if not existing_user:
        new_user = User(user_id=message.from_user.id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        last_name=message.from_user.last_name,
                        language_code=message.from_user.language_code)
        session.add(new_user)
    session.commit()


@dp.message(Command('help'))
async def helps(message: types.Message):
    await bot.send_message(message.chat.id, "Список всех доступных комманд:\n/create - Создать игру.\n/join <ID> \
- Подключится к существующей игре.\n/exit - Выйти из игры.")


async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
