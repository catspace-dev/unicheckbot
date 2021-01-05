from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from loguru import logger


class LoggingMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        logger.info(f"User {message.from_user.id} issued command: {message.text}")
