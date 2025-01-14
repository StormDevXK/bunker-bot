import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.future import select
from model import User, Lobby, LobbyPlayer, Characteristic, Catastrophe, users_engine, Base, async_session_maker


# Иницализация
async def init_db():
    async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Сохранение данных пользователя в бд, если их там нет
async def save_user_data_to_db(message):
    async with async_session_maker() as session:
        query = select(User).where(message.from_user.id == User.telegram_id)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if not existing_user:
            new_user_data = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=f"{message.from_user.first_name} {message.from_user.last_name}" if message.from_user.last_name else message.from_user.first_name,
                created_at=datetime.datetime.now()
            )
            session.add(new_user_data)
            await session.commit()
