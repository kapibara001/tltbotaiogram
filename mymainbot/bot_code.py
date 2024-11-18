from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
a = 0

bot = Bot("7381967574:AAG5AFZjoYqJOml34yQKLE9boCSH96Y1ALM")
dp = Dispatcher(bot)

class Form(StatesGroup):
    pere = State()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Здравствуйте! Вот команды для пользования этим ботом:\n/start - Запуск бота\n/socials - Открыть меню пользования соц-сетями\n/timer - ....")

@dp.message_handler(commands=['socials'])
async def start_cmd(message: types.Message):
    markup_inl = types.InlineKeyboardMarkup() 
    markup_rpl = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    
    yt = types.InlineKeyboardButton("YouTube", url="https://www.youtube.com/", callback_data="1")
    tg = types.InlineKeyboardButton("Telegram", url="https://web.telegram.org/a/", callback_data="2")
    vk = types.InlineKeyboardButton("VKontakte", url="https://vk.com/feed", callback_data="3")
    
    markup_inl.row(yt, tg)
    markup_inl.row(vk)
       
    ytt = types.KeyboardButton("YouTube", web_app=WebAppInfo(url='https://www.youtube.com/'))
    tgg = types.KeyboardButton("Telegram", web_app=WebAppInfo(url='https://web.telegram.org/a/'))
    vkk = types.KeyboardButton("VK", web_app=WebAppInfo(url='https://vk.com/feed'))
    
    markup_rpl.row(ytt, tgg)
    markup_rpl.row(vkk)
    
    await message.reply("Вот список соц-сетей. Нажмите на кнопку, чтобы перейти.", reply_markup=markup_inl)
    await message.answer("Также вы можете открыть прилжение соц-сети прямо здесь.", reply_markup=markup_rpl)

@dp.message_handler(commands=['timer'])
async def random(message: types.Message):
    await message.answer(message.chat.id, 'Напиши количество секунд, которое вы хотите засечь! ')
    await Form.pere.set()

@dp.message_handler(state=Form.a)
async def random_2(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        a['pere'] = message.text
        await message.reply(f'Вы засекли {a} cекунд!')
        await state.finish()
    
    
    



executor.start_polling(dp)