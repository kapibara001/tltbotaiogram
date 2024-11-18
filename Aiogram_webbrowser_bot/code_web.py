from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot("7252694080:AAHKDAlIndUb5a7SsKCaVL5YjXnpau9Dg8E")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton("Открыть веб-страницу", web_app=WebAppInfo(url="https://kapibara001.github.io/sitesite/")))#Создали открывающееся окошко после нажатия на кнопку
    
    await message.reply("Привет! Ссылка под сообщением. ", reply_markup=markup)



executor.start_polling(dp)