import telebot, webbrowser, time, sqlite3, requests, json
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot("7284959977:AAElpOdMiL3wSMhPMsbG3kGTJRA1gmJLHfc") #Save our token
api = "6a60b4e0cbf73adcd38a36d5a32fb466"
first_name = ''
last_name = ''
link = ''
user_num = 0
currency = CurrencyConverter()

#-----------------------------------------------------


@bot.message_handler(commands=['start']) #Обработка команды /start. Чтобы эта функция срабатывала при нескольких коммандах, то после 'start' достаточно прописать еще команду 
def hello(message): #функция хранит онформацию про пользователя и сам чат
    bot.send_message(message.chat.id, f'Приветствую тебя в этом чате, <B>{message.from_user.first_name}</B>!\n'
'Помощь в общении - <b>/help</b>.', parse_mode='HTML') #Отправка пользлователю сообщение. message.chat.id указывает айди чата с которым мы взаимодействуем


@bot.message_handler(commands=['weather'])
def weather_inf(message):
    bot.send_message(message.chat.id, "Напиши город, в котором хочешь узнать погоду.")

    bot.register_next_step_handler(message, api_weather)


def api_weather(message):
    city = '' 
    city = message.text.strip()
    
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')

    #city = city[0].upper()+city[1:-1]
    if res.status_code == 200:
        weath = json.loads(res.text)
        temp = weath["main"]["temp"]

        bot.reply_to(message, f'Погода в городе {city}: {temp} градусов Цельсия.')
    else:
        bot.reply_to(message, "Город не найден.")

@bot.message_handler(commands=['login'])
def my_info(message):
    bot.send_message(message.chat.id, f'Ваш id: <b>{message.from_user.id}</b>\n'
                                      f'Ваше отображаемое имя: <b><u>{message.from_user.first_name}</u></b>\n'
                                      f'Ваше имя пользователя: <b><u>{message.from_user.username}</u></b>\n',
                                      parse_mode="HTML") #С помощью parse_mode можно кастомизировать текст, например тут мы взяли кастомизацию из HTML.

@bot.message_handler(commands=['allinf'])
def allinf(message):
    btn = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Вперед", callback_data="None")
    btn2 = types.InlineKeyboardButton("Назад", callback_data="None")
    btn.row(btn1, btn2)
    bot.send_message(message.chat.id, message, reply_markup=btn)

@bot.message_handler(commands=['link'])
def link_func(message):
    global link
    bot.send_message(message.chat.id, "Отправте мне ссылку и я вас туда перенаправлю!")
    bot.register_next_step_handler(message, net_link)

def net_link(message):
    link = message.text

    link_btn = types.InlineKeyboardMarkup()
    link_btn.add(types.InlineKeyboardButton("Ссылка", url=str(link)))

    bot.send_message(message.chat.id, "Можете переходить ->", reply_markup=link_btn)

@bot.message_handler(commands=['site'])
def open_site(message):
    btns_row1 = types.InlineKeyboardMarkup()

    yt = types.InlineKeyboardButton("YouTube", "youtube.com")
    ggle = types.InlineKeyboardButton("Google", "google.com")
    tlgm = types.InlineKeyboardButton("Telegram", "telegram.org")
    Vk = types.InlineKeyboardButton("VK", "VK.com")

    btns_row1.row(yt, ggle)
    btns_row1.row(tlgm, Vk)
    btns_row1.add(types.InlineKeyboardButton("Назад", callback_data="None"))

    bot.send_message(message.chat.id, "Выберите сайт, который вы хотите открыть.", reply_markup=btns_row1)
    
@bot.message_handler(commands=['convert'])
def start_conv(message):
    bot.send_message(message.chat.id, "Введите любое число некоторой валюты, которую хотите конвертровать")
    bot.register_next_step_handler(message, convertation_1)

def convertation_1(message):
    global user_num
    try:
        user_num = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели не число, попрообуйте снова!")
        bot.register_next_step_handler(message, convertation_1)
        return

    if user_num > 0:
        btns = types.InlineKeyboardMarkup(row_width=2)

        btns_1 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
        btns_2 = types.InlineKeyboardButton("USD/RUB", callback_data="USD/RUB")
        btns_3 = types.InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
        btns_4 = types.InlineKeyboardButton("USD/CNY", callback_data="USD/CNY")
        btns_5 = types.InlineKeyboardButton("CNY/USD", callback_data="CNY/USD")
        btns_else = types.InlineKeyboardButton("Другое", callback_data="else")

        btns.add(btns_1, btns_2, btns_3, btns_4, btns_5, btns_else)

    else:
        bot.send_message(message.chat.id, "Данное число нельзя конвертировать так как оно <= 0.\n\nНапишите неотрицательное число, отличное от нуля!")
        bot.register_next_step_handler(message, convertation_1)
        return

    bot.reply_to(message, "Из какой валюты в какую хотите конвертировать стоимость?", reply_markup=btns)

@bot.callback_query_handler(func=lambda call: True)
def callback_1(call):
    if call.data != "else":
        values = call.data.upper().split('/')
        result = currency.convert(user_num, values[0], values[1])
        bot.send_message(call.message.chat.id, f'{user_num} {values[0]}: {round(result, 2)} {values[1]}.')
        bot.send_message(call.message.chat.id, "Вы можете написать новое число, если хотите.")
        bot.register_next_step_handler(call.message, convertation_1)
    else:
        bot.send_message(call.message.chat.id, "Напишите из какой валюты в какую хотите перевести международными названиями через слэш. Например: CNY/USD.")
        bot.register_next_step_handler(call.message, if_else_conv)

def if_else_conv(message):
    values = message.text.strip().upper().split('/')
    result = currency.convert(user_num, values[0], values[1])
    bot.send_message(message.chat.id, f'{user_num} {values[0]}: {round(result, 2)} {values[1]}.')
    bot.send_message(message.chat.id, "Вы можете написать новое число, если хотите.")
    bot.register_next_step_handler(message, convertation_1)
   



@bot.message_handler(commands=['register'])
def infos(message):
    base = sqlite3.connect("base_users.sql")
    base_curs = base.cursor()

    base_curs.execute('CREATE TABLE IF NOT EXISTS users_list(id int auto_increment primary key, first_name varchar(50), last_name varchar(50), age int)')
    base.commit()
    base_curs.close()
    base.close()

    bot.send_message(message.chat.id, "Сейчас будет проихсодить регистрация пользователя. Просьба вводить то, что от вас будут просить в сообщении. ")
    bot.send_message(message.chat.id, "Введите ваше <u><b>имя</b></u>:", parse_mode="HTML")
    bot.register_next_step_handler(message, first_name_func)

def first_name_func(message):
    global first_name
    first_name = message.text.strip()
    
    bot.send_message(message.chat.id, "Введите вашу фамилию:")
    bot.register_next_step_handler(message, last_name_func)

def last_name_func(message):
    global last_name
    last_name = message.text.strip()
    
    bot.send_message(message.chat.id, "Введите ваш возраст:")
    bot.register_next_step_handler(message, age_func)

def age_func(message):
    age = message.text.strip()

    base = sqlite3.connect("base_users.sql")
    base_curs = base.cursor()

    base_curs.execute('INSERT INTO users_list(first_name, last_name, age) VALUES("%s", "%s", "%s")' % (first_name, last_name, age))
    base.commit()
    base_curs.close()
    base.close()

    inf = types.InlineKeyboardMarkup()
    inf.add(types.InlineKeyboardButton("Все пользователи", callback_data="all_inf"))



    bot.send_message(message.chat.id, "Ваши данные внесены в базу. Нажмите кнопку снизу, чтобы проверить.", reply_markup=inf)

@bot.callback_query_handler(func=lambda call: True)
def enter_inf(call):
    if call.data == "all_inf":
        base = sqlite3.connect("base_users.sql")
        base_curs = base.cursor()

        base_curs.execute('SELECT * FROM users_list')
        users = base_curs.fetchall()

        info = ''
        k = 0
        for i in users:
            k+=1
            info += f'{k}. Полное имя: {i[1]} {i[2]}. Возраст: {i[-1]}\n\n'

        base_curs.close()
        base.close()

        bot.send_message(call.message.chat.id, info)

@bot.message_handler(commands=['help'])
def help_def(message):
    bot.send_message(message.chat.id, "Команды для общения в чате:\n\
/start - начало общения.\n\
/login - ваш id, ваше отображаемое имя, ваш логин.\n\
/allinf - информация для разработчика.\n\
/site - открыть вкладки в интернете.\n\
/register - регистрация в боте.\n\
/link - открыть ссылку.\n\
/weather - узнать погоду в интересующем вас городе.\n\
/convert - узнать курс актуальной валюты.\n\
/help - помощь в общении.")

#--------------------------------------------------------------------------------------------

#Обработка не команды, а обычного сообщения. Такие нужно обрабатывать после команд, иначе команды работать не будут
#или же 





bot.polling(non_stop=True) #Делаем работу нашего бота бесконечной. Еще есть команда bot.infinity_polling()
#bot.infinity_polling()