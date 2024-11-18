import telebot
from telebot import types

bot = telebot.TeleBot("6138550245:AAGr1-jUwq0GceGNnvYTf9NezrwZhC5Gjls")

#Команды_____________________________________________

@bot.message_handler(commands=['start'])
def start_cmd(message):
    btns = types.ReplyKeyboardMarkup() #Создаем кнопки, которые идут не под сииобщениями, а под чатом самим

    btn1 = types.KeyboardButton("Изменить текст")
    btn2 = types.KeyboardButton("Удалить фото")

    btns.row(btn1, btn2)

    mora = open('./main.jpg', "rb") # Должно работать, но почему то не хочет находить фотку
    bot.send_photo(message.chat.id, mora, reply_markup=btns)
    #bot.send_message(message.chat.id, "Привет", reply_markup=btns)
    bot.register_next_step_handler(message, on_click) #Мы как бы зарегистрировали, что после нажатия этой кнолпки будет происходить функция on_click

def on_click(message):
    if message.text == "Изменить текст":
        bot.send_message(message.chat.id, "No")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Deleted")


#Обычные сообщения______________________________________




#Фото, видео, аудио________________

@bot.message_handler(content_types=['photo'])
def photo_check(message):
    markup = types.InlineKeyboardMarkup() #Создаем объект самой кнопки под сообщением

    #markup.add(types.InlineKeyboardButton("хх.ру", url= "hh.ru")) #Добавляем к объекту кнопку хх.ру с ссылкой hh.ru

    btn1 = types.InlineKeyboardButton("YouTube", url= "YouTube.com")
    btn2 = types.InlineKeyboardButton("Google", url="google.com")
    btn3 = types.InlineKeyboardButton("Telegram", url="web.telegram.org")
    markup.row(btn1, btn2, btn3)

    markup.add(types.InlineKeyboardButton("Удалить фото", callback_data="delete")) #Через callback_data мы присваиваем кнопке какое-то действие
    markup.add(types.InlineKeyboardButton("Изменить текст", callback_data="edit"))
    bot.reply_to(message, "Фото принято.", reply_markup=markup) #Омвечаем на сообщение, прикрепляя кнопки к нему.

@bot.callback_query_handler(func=lambda callback: True) #Данный декоратор обратабывает события, заключенные в callback_data.
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id) #мы обращаемся к сообщению, которое пришло в ответ, поэтому везде добавляется callback перед message



bot.polling(none_stop=True)