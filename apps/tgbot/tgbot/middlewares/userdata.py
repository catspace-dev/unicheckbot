from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from tgbot.models import User


def userdata_required(func):
    """Setting login_required to function"""
    setattr(func, 'userdata_required', True)
    return func


class UserMiddleware(BaseMiddleware):

    def __init__(self):
        super(UserMiddleware, self).__init__()

    @staticmethod
    async def get_userdata(telegram_id: int) -> User:
        handler = current_handler.get()
        if handler:
            attr = getattr(handler, 'userdata_required', False)
            if attr:
                # Setting user
                user, _ = await User.get_or_create(telegram_id=telegram_id)
                return user

    async def on_process_message(self, message: Message, data: dict):
        data['user'] = await self.get_userdata(message.from_user.id)

    async def on_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        data['user'] = await self.get_userdata(callback_query.from_user.id)
