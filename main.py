from os import getenv
from os.path import exists
from dotenv import load_dotenv
if exists(".env"):
    load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Hello")


@dp.message(Command('help'))
async def helps(message: types.Message):
    await bot.send_message(message.chat.id, "You really need help?🥲")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
