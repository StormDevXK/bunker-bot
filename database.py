import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
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


# Модель для таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(64), unique=True, nullable=False)
    username = Column(String(32))
    full_name = Column(String(128))
    created_at = Column(DateTime, nullable=False)

    lobbies = relationship("LobbyPlayer", back_populates="user")

# Модель для таблицы lobbies
class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True)
    catastrophe_id = Column(Integer, ForeignKey("catastrophe.id"), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)

    players = relationship("LobbyPlayer", back_populates="lobby")
    catastrophe = relationship("Catastrophe", back_populates="lobbies")

# Модель для таблицы lobby_players
class LobbyPlayer(Base):
    __tablename__ = "lobby_players"

    id = Column(Integer, primary_key=True)
    lobby_id = Column(Integer, ForeignKey("lobbies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profession_id = Column(Integer, ForeignKey("characteristics.id"))
    is_profession_visible = Column(Boolean, default=False)
    sex_id = Column(Integer, ForeignKey("characteristics.id"))
    is_sex_visible = Column(Boolean, default=False)
    health_id = Column(Integer, ForeignKey("characteristics.id"))
    is_health_visible = Column(Boolean, default=False)
    body_type_id = Column(Integer, ForeignKey("characteristics.id"))
    is_body_type_visible = Column(Boolean, default=False)
    phobia_id = Column(Integer, ForeignKey("characteristics.id"))
    is_phobia_visible = Column(Boolean, default=False)
    hobby_id = Column(Integer, ForeignKey("characteristics.id"))
    is_hobby_visible = Column(Boolean, default=False)
    fact_id = Column(Integer, ForeignKey("characteristics.id"))
    is_fact_visible = Column(Boolean, default=False)
    inventory_id = Column(Integer, ForeignKey("characteristics.id"))
    is_inventory_visible = Column(Boolean, default=False)

    lobby = relationship("Lobby", back_populates="players")
    user = relationship("User", back_populates="lobbies")

# Модель для таблицы characteristics
class Characteristic(Base):
    __tablename__ = "characteristics"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)

# Модель для таблицы catastrophe
class Catastrophe(Base):
    __tablename__ = "catastrophe"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty_level = Column(Integer, nullable=False)

    lobbies = relationship("Lobby", back_populates="catastrophe")


# Иницализация
async def init_db():
    async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Сохранение данных пользователя в бд, если их там нет
async def save_user_data_to_db(message):
    async with async_session_maker() as session:
        query = select(User).where(User.telegram_id == message.from_user.id)
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
