from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from database import init_db, User, get_db
from sqlalchemy.orm import Session

from dotenv import load_dotenv #для работы с сессиями БД
import os

from middlewares.db import DatabaseSessionMiddleware

#from aiogram import Router
import asyncio

# Инициализация базы данных
init_db()

# Инициализация бота
load_dotenv() 
TOKEN = os.getenv("BOT_TOKEN") #подгружаем токен из .env

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_cmd(message: Message, db: Session):

    if not message.from_user:#проверка на успешное получение информации из сообщения пользователя
        await message.answer("Не удалось получить информацию о пользователе")
        return

    user = db.query(User).filter(User.user_id == message.from_user.id).first() #ищем пользователя в базе
    
    if not user:
        new_user = User (
            user_id = message.from_user.id,
            username =  message.from_user.username,
            created_at = str(message.date)
        )
        db.add(new_user)
        db.commit()
        
        await message.answer("Добро пожаловать! Вы были зарегистрированы в системе.")
    else:
        await message.answer("С возвращением!")

    await message.answer("Я бот, помогающий с продажами на WB")

# Обработчик команды /set_api
@dp.message(Command("set_api"))
async def set_api_cmd(message: Message, db: Session):
    if not message.text or not message.from_user:#проверка на успешное получение информации из сообщения пользователя
        await message.answer("Не удалось получить информацию о пользователе")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /set_api <ваш_api_ключ>")
        return
    
    api_key = args[1]
    user = db.query(User).filter(User.user_id == message.from_user.id).first()
    
    if user:
        if not isinstance(api_key, str):
            user.api_key = str(api_key)
        db.commit()
        await message.answer(f"API-ключ успешно сохранен: {api_key}")
    else:
        await message.answer("Сначала зарегистрируйтесь с помощью /start")

# Запуск бота
async def main():
    dp.message.middleware(DatabaseSessionMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())