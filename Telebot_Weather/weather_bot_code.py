import telebot, requests, json

bot = telebot.TeleBot("7189540792:AAFT_IiF4em8HL-38CH74Uzv5KMIRDqHWlE")
api = "6a60b4e0cbf73adcd38a36d5a32fb466"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, рад тебя видеть! Напиши название города, чтобы узнать в нем погоду!")

@bot.message_handler(content_types=['text']) # На вход поступает сообщение с типом ТЕКСТ. НЕ КОМАНДА, а простое сообщение
def get_weather(message):
    city = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
    if res.status_code == 200: #Если запрос верный, то всегда будет код 200, другой код обозначает ошибку
        data = json.loads(res.text) # Заключаем нашу инфу в переменную, отформотировав в нужный нам формат
        temp = data["main"]["temp"]
        #country = data["sys"]["country"]
        bot.reply_to(message, f'Погода в городе {city}: {temp} °С.') # Благодаря

        image = 'Photo/sunny.png' if temp > 20.0 else 'Photo/bad_ewather.jpg'
        file = open(image, 'rb')
        bot.send_photo(message.chat.id, file)
    
    else:
        bot.reply_to(message, f'Город указан неверно.')



 



bot.polling(none_stop=True)