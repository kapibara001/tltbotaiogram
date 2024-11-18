import telebot, sqlite3, webbrowser
from telebot import types

bot = telebot.TeleBot("7357206445:AAFv225Fo1gbwGBodmII1cIqEha2s2iFgSQ")
name = "None"

@bot.message_handler(commands=['start'])
def start_def(message):
    con = sqlite3.connect('baza.sql') #Созданеие !файла! базы данных, !не самой базы! c именем в скорбках. 
                                      #Если ее не было, она создается, если была, то ничего не проиходит

    cur = con.cursor() #Создание курсора, с помощью которого будет происходить управление базой

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50), pass varchar(50))') 
    # Cоздание базы в том случае, если она не была создана до этого 
    # Создаем таблицу users, в которой есть поля с id(имеющий тип целого числа, автоматически изменяющееся(primary)),
    # поле name, хранящее имя в типе varchar с длиной 50 символов, с паролем также

    con.commit() #Сохраняет изменения. Нужно писать когда идет имзенение базы данных, а когда просто выдача данных из нее,
                 #писать ее  не обязательно. Окончательное создание в случае если не создана еще. 

    cur.close() # Выключение возможности управлять базой
    con.close() # Отключение подключения к базе.

    bot.send_message(message.chat.id, "Введите имя")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip() # Берем Имя, которое вводит пользователь в своем сообщении

    bot.send_message(message.chat.id, "Введите Пароль")
    bot.register_next_step_handler(message, user_password)

def user_password(message):
    password = message.text.strip() # Берем пароль, которое вводит пользователь в своем сообщении

    con = sqlite3.connect('baza.sql') 
    cur = con.cursor() 

    cur.execute('INSERT INTO users (name, pass) VALUES("%s", "%s")' % (name, password)) # Вписываем в базу данных данные имени и пароля 
    con.commit()
    cur.close()
    con.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Список пользователей", callback_data="chat_users_list"))

    bot.send_message(message.chat.id, "Пользователь зарегистрирован", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    con = sqlite3.connect('baza.sql') #Созданеие базы данных
    cur = con.cursor() #Создание курсора, с помощью которого будет происходить управление базой

    cur.execute('SELECT * FROM users')
    users = cur.fetchall() #Функция вернет нам все найденные записи

    info = ''
    k = 0
    for i in users:
        k += 1
        info += f'ID: {k}. Имя: {i[1]}. Пароль: {i[2]}\n'

    cur.close()
    con.close()

    bot.send_message(call.message.chat.id, info)
    bot.send_message(call.message.chat.id,  f'Всего пользователей: {k}')



bot.polling(none_stop=True)