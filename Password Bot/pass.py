import telebot, sqlite3
from telebot import types
from uuid import uuid4
platform = ''
login = ''
password = ''
bot = telebot.TeleBot("7320927907:AAEnlwGsmY6kQ9dPuMttkOQFgnvU9kLcOE4")

@bot.message_handler(commands=['start'])
def hello(message):
    db_passwords = sqlite3.connect("passwords_list.sql")
    curs = db_passwords.cursor()
    
    curs.execute('CREATE TABLE IF NOT EXISTS passwords(id_user int auto_increment primary key, platform varchar(50), login varchar(50), password varchar(50))')
    db_passwords.commit()
    
    curs.close()
    db_passwords.close()
    
    bot.send_message(message.chat.id, "<B>Привет!</B>\nНовый пароль: /newpass\nСписок паролей: /allpass\n", parse_mode="HTML")
    
@bot.message_handler(commands=['allpass'])
def allp(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Удалить строку", callback_data='2'))
        
        db_passwords = sqlite3.connect("passwords_list.sql")
        curs = db_passwords.cursor()
        
        curs.execute('SELECT * FROM passwords')
        data = curs.fetchall()
            
        info = ''
        number = 0
        for i in data:
            number += 1
            info += f'{number}) Платформа: {i[1]}.\n Логин: {i[2]}.\n Пароль: {i[3]}.\n\n'
            
        bot.send_message(message.chat.id, info, reply_markup=markup)
            
        curs.close()
        db_passwords.close()

        
    except Exception:
        bot.send_message(message.chat.id, "Скорее всего у вас нет ни одного пароля, время добавить его!")
    
@bot.message_handler(commands=['newpass'])
def reg_mes_1(message):
    bot.send_message(message.chat.id, "Отлично! Вы начали регистрацию нового пароля для очередной платформы.\n\
Сначала введите платформу, от которой хотите запомнить пароль.")
    bot.register_next_step_handler(message, reg_mes_platform)
    
def reg_mes_platform(message):
    global platform
    platform = message.text.strip() 
    bot.reply_to(message, "Отлично! Теперь напишите почту/логин для входа на платформу.")
    bot.register_next_step_handler(message, reg_mes_login)
    
def reg_mes_login(message):
    global login
    login = message.text.strip() 
    bot.reply_to(message, "Просто прекрасно! Можете ввести пароль и регистрация профиля на сайте будет завершена!")
    bot.register_next_step_handler(message, reg_mes_pass)

def reg_mes_pass(message):
    global password
    password = message.text.strip()    

    db_passwords = sqlite3.connect("passwords_list.sql")
    curs = db_passwords.cursor()
    
    curs.execute('INSERT INTO "passwords" (id_user, platform, login, password) VALUES ("%s", "%s", "%s", "%s")' % (str(uuid4), platform, login, password))
    db_passwords.commit()
    curs.close()
    db_passwords.close()
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Пароли", callback_data='1'))
    markup.add(types.InlineKeyboardButton("Удалить строку", callback_data='2'))
    bot.send_message(message.chat.id, "Ваш пароль записан в БД!", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call:True)
def call_back(call):
    if call.data == '1':
        db_passwords = sqlite3.connect("passwords_list.sql")
        curs = db_passwords.cursor()
    
        curs.execute('SELECT * FROM passwords')
        data = curs.fetchall()
        
        info = ''
        #number = 0
        for i in data:
            #number += 1
            info += f'{i[0]}") Платформа: {i[1]}.\n Логин: {i[2]}.\n Пароль: {i[3]}.\n\n'
        
        bot.send_message(call.message.chat.id, info)
        
        curs.close()
        db_passwords.close()
        
    if call.data == '2':
        bot.send_message(call.message.chat.id, "Строку с каким номером вы хотите удалить?")
        bot.register_next_step_handler(call.message, delete)
    
def delete(message):
    num = message.text
    db_passwords = sqlite3.connect("passwords_list.sql")
    curs = db_passwords.cursor()
    
    try:
        curs.execute(f'DELETE FROM passwords WHERE Id=1')
        
    except Exception:
        bot.send_message(message.chat.id, "Возможно вы указали неверный номер регистрационного пароля. Попробуйте снова!")
                    
        curs.close()
        db_passwords.close()
        
        bot.register_next_step_handler(message, delete)
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Пароли", callback_data='1'))
    
    bot.send_message(message.chat.id, "Пароль успешно удален!", reply_markup=markup)
    curs.close()
    db_passwords.close()
    
bot.polling(non_stop=True)