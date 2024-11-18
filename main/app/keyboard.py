from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo


cars_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Porshe 911', callback_data='prhe'), InlineKeyboardButton(text='Mercedes-Benz G63', callback_data='G63')],
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data='back')]
])

yout = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Youtube", web_app=WebAppInfo(url='https://www.youtube.com/'))]
])