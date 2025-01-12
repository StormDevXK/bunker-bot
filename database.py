import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# Инициализация SQLAlchemy для работы с базой данных
DATABASE_URL = "sqlite+aiosqlite:///bot.db"
users_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Настройка асинхронной сессии
async_session_maker = sessionmaker(
    bind=users_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Определение модели пользователя
class UserData(Base):
    __tablename__ = "users_data"

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
