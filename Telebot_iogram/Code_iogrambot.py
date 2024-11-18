from aiogram import Bot, Dispatcher, types, executor

bot = Bot("6702625347:AAG3lNt1HULxBAPTVn8NUV8pTNlHVDhZS7g") #аналог telebot.Telebot(""), то есть подключение бота
dp  = Dispatcher(bot) # Вприницпе работа с ботом: отслежитвание, отправка сообщений и тп.

@dp.message_handler(commands=['start'])
async def start(message: types.Message): # В aiogram все функции ассинхронны, то есть функция, которая может быть запущена когда угодно во время выполнения кода
    await message.answer("Старт!")

@dp.message_handler(content_types=['photo'])
async def st_ph(message: types.Message):
    await message.reply("Фото!")
    
@dp.message_handler(commands=['inline'])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    markup.add(types.InlineKeyboardButton('site', url= 'google.com'))
    markup.add(types.InlineKeyboardButton('Кнопка', callback_data='1'))
    markup.add(types.InlineKeyboardButton('Кнопка2', callback_data='2'))
    
    await message.answer("Отлично! ", reply_markup=markup)
    
@dp.callback_query_handler()
async def callback(call):
    if call.data == "1":
        await call.message.answer("Колбэк 1 - " + call.data)  
    elif call.data == "2":
        await call.message.reply("Колбэк 2 - " +call.data)
    
    
@dp.message_handler(commands=['reply'])
async def button_cmd(message: types.Message):
    btn = types.ReplyKeyboardMarkup(one_time_keyboard=True) # Это свойство нужно для того, чтобы кнопки показывались только 1 раз, затем скрывались
    
    btn.add(types.KeyboardButton("Мама"))
    btn.add(types.KeyboardButton("Папа"))
    
    await message.answer("commands=['reply']", reply_markup=btn)
    
@dp.message_handler(content_types=['text'])
async def check(message: types.Message):
    if message.text == "Мама":
        await message.reply("Все хорошо")
    if message.text == "Папа":
        await message.reply("Он гигачад")



executor.start_polling(dp) # аналог bot.polling(none_stop=True)
 

#bot= telebot.TeleBot("6702625347:AAG3lNt1HULxBAPTVn8NUV8pTNlHVDhZS7g") В aiogram используется немного другой синтаксис, эти команды там неактуальны.
#bot.polling(none_stop=True) 