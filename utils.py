from os import getenv
from os.path import exists
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env, если он существует
if exists(".env"):
    load_dotenv()

# Определение токена бота
BOT_TOKEN: str = getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверьте файл .env или переменные окружения.")
