import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from utils import BOT_TOKEN
from handlers import start_handler, help_handler
from database import init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
dp.message.register(start_handler, Command("start"))
dp.message.register(help_handler, Command("help"))


# Основной цикл
async def main():
    await init_db()  # Инициализация базы данных
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
