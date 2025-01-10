from os import getenv
from os.path import exists
import asyncio
import datetime

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command


from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


if exists(".env"):
    load_dotenv()


users_engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Session = sessionmaker(bind=users_engine)
session = Session()


class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now)


Base.metadata.create_all(users_engine)


BOT_TOKEN: str = getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Добро пожаловать в бункер!\nЧтобы начать играть нужно создать лобби \
- /create\nИли подключится к уже созданному - /join <ID>\nЕсли возникнут вопросы - /help")

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
