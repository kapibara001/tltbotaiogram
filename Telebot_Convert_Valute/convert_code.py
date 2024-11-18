import telebot
from currency_converter import CurrencyConverter
from telebot import types
amount = 0

bot = telebot.TeleBot("7255190952:AAERUwochWHWgpt3MQwj1t-UD8YGE4GO4OI")
currency = CurrencyConverter()

@bot.message_handler(commands=["start"])
def start_com(message):
    bot.send_message(message.chat.id, "Здравствуйте, введите сумму.")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.reply_to(message, "Вы ввели не число. Попробуйте снова.")
        bot.register_next_step_handler(message, summa)
        return
    
    if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2) #В скобках задали максималоьное количество элементов в одном ряду

            btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
            btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
            btn3 = types.InlineKeyboardButton("USD/RUB", callback_data="usd/rub")
            btn4 = types.InlineKeyboardButton("RUB/USD", callback_data="rub/usd")
            btn5 = types.InlineKeyboardButton("Другое", callback_data="else")

            markup.add(btn1, btn2, btn3, btn4, btn5) #У нас образовываются линии по 2 кнопки из-за ограничения
    else:
        bot.reply_to(message, "Несуществующее значение для конвертации. Попробуйте снова")
        bot.register_next_step_handler(message, summa)
        return

    bot.send_message(message.chat.id, "Что и в какую валюту вы хотите конвертрировать?(Что/Куда)", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару валют через '/', например: (EUR/USD).")
        bot.register_next_step_handler(call.message, else_value)

def else_value(message):
    try:
        any_v = message.text.strip().upper().split('/')
        res = currency.convert(amount, any_v[0], any_v[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception: # В случае возникновения ЛЮБОЙ ошибки
        bot.send_message(message.chat.id, "Что-то пошло не так... Впишите ваши валюты для конвертации заново в формате */*.")
        bot.register_next_step_handler(message, else_value)
        return






bot.polling(none_stop=True)