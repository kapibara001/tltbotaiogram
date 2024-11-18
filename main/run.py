import asyncio

from aiogram import Dispatcher, Bot
from cfg import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router) # подключение "одного конца провода" к роутеру
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")