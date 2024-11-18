from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboard as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middleware import TestMiddleWare

router = Router()

router.message.outer_middleware(TestMiddleWare())

class Reg(StatesGroup):
    name = State()
    number = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Помощь: /help")

@router.message(Command('help'))
async def help(message: Message):
    await message.answer("/start - начать\n\
/reg - регистрация\n\
/help - помощь\n\
/cars - автомобили\n\
/planes - самолеты\n")
    
@router.message(Command('cars'))
async def cars(message: Message):
    await message.answer("Список доступных автомобилей:", reply_markup=kb.cars_btn)

@router.callback_query(F.data == "prhe")
async def porsche(callback: CallbackQuery):
    await callback.message.edit_text("<B>Название автомобиля</B>: Porsche 911 (992) открытый кузов.\n\
<B>Год выпуска</B>: 2022\n\
<B>Объем двигателя</B>: 3.0 л\n\
<B>Мощность двигателя</B>: 480 л.с.\n\
<B>Тип топлива</B>: бензин\n\
<B>Коробка передач</B>: робот\n\
<B>Привод</B>: полный привод (4WD)", parse_mode="HTML", reply_markup=kb.back)

@router.callback_query(F.data == "G63")
async def porsche(callback: CallbackQuery):
    await callback.message.edit_text("Название автомобиля: Mercedes-Benz G63 AMG Mesnsory\n\
Год выпуска: 2024\n\
Объем двигателя: 5.0 л\n\
Мощность двигателя: 585 л.с.\n\
Тип топлива: бензин\n\
Коробка передач: робот\n\
Привод: полный привод (4WD)", reply_markup=kb.back)
      
@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Список доступных автомобилей:", reply_markup=kb.cars_btn)

@router.message(Command('reg')) 
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name) # Активация состояния класса Reg, где мы работает с полем name
    await message.answer("Введите свое имя") 

@router.message(Reg.name) # Сама работа с полем name
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text) # Обновление информации в поле name класса Reg
    await state.set_state(Reg.number) # Активация состояния класса Reg, где мы работает с полем number
    await message.answer("Введите свой номер телефона") 

@router.message(Reg.number)
async def two_three(message: Message, state=FSMContext):
    await state.update_data(number=message.text) # Обновление информации в поле number класса Reg
    data = await state.get_data() # сохранение данных в переменную data
    await message.answer(f'Спасибо, регистрация завершена.\nИмя: {data["name"]}\nНомер: {data["number"]}')
    await state.clear() # Очистка состояний

@router.message(Command('youtube'))
async def yt(message: Message):
    await message.reply("Ютуб открывается в отдельном окне", reply_markup=kb.yout)

