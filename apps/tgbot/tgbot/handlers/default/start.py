from aiogram.types import Message


async def start_cmd(msg: Message):
    await msg.answer("Basic reply")