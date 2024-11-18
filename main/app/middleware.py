from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class TestMiddleWare(BaseMiddleware): # создание дочернего класса по отношению к BaseMiddleware 
    async def __call__(self,   # метод call, который принимает следующие параметры
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        print("Действия до обработчика")
        result = await handler(event, data)
        print("Действия после обработчика")
        return result