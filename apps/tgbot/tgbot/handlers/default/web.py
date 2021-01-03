from aiogram.types import Message
from typing import Optional
from tgbot.handlers.helpers import check_int
from tgbot.nodes import nodes
import httpx

help_message = """
Использование:
 /web <hostname> <port> 
 /web <hostname>
 
 Производит проверку хоста по протоколу HTTP.
"""

invalid_port = """Неправильный порт!"""


async def check_web(message: Message, host: str, port: Optional[int]):
    if port is None:
        port = 80
    responses = []
    for node in nodes:
        async with httpx.AsyncClient() as client:
            result = await client.get(
                f"{node.address}/http", params=dict(
                    target=host,
                    port=port,
                    token=node.token
                )
            )
            await message.answer(result.json())
            responses.append(result)

    await message.answer(f"{host}:{port}")


async def web_cmd(msg: Message):

    port = None
    # TODO: Maybe check it in separated function?
    args = msg.text.split(" ")
    if len(args) < 2:
        return await msg.answer(help_message)
    if len(args) == 3:
        port = args[2]
        if not check_int(port):
            return await msg.answer(invalid_port)
    host = args[1]

    await check_web(msg, host, port)

