import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.future import select

# Инициализация SQLAlchemy для работы с базой данных
DATABASE_URL = "sqlite+aiosqlite:///bot.db"
users_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Настройка асинхронной сессии
async_session_maker = async_sessionmaker(
    bind=users_engine,  # Инициализация асинхронного движка базы данных
    class_=AsyncSession,  # Класс для асинхронных сессий
    expire_on_commit=False
)


# Создание класса данных пользователя
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now)


# Иницализация
async def init_db():
    async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Сохранение данных пользователя в бд, если их там нет
async def save_user_data_to_db(message):
    async with async_session_maker() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalars().first()

        if not existing_user:
            new_user_data = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code
            )
            session.add(new_user_data)
            await session.commit()
