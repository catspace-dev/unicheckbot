from aiogram.types import Message
from loguru import logger


async def start_cmd(msg: Message):
    logger.info(f"{msg.from_user.full_name} send /start")
    await msg.answer("Basic reply")