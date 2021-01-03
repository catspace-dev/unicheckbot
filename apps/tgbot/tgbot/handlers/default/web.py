from aiogram.types import Message
from typing import Optional
from tgbot.handlers.helpers import check_int
from tgbot.nodes import nodes
from httpx import AsyncClient, Response
from core.coretypes import ResponseStatus, HTTP_EMOJI
from datetime import datetime

web_help_message = """
❓ Производит проверку хоста по протоколу HTTP.

Использование:
 `/web <hostname> <port>` 
 `/web <hostname>` - автоматически выставит 80 порт
"""

invalid_port = """❗Неправильный порт. Напишите /web чтобы увидеть справку к данному способу проверки."""


async def prepare_webcheck_message(response: Response) -> str:
    # TODO: Use types from core!
    message = ""
    json_rsp = response.json()
    status = json_rsp.get("status")
    location = json_rsp['node']['location']
    if status == ResponseStatus.OK:
        status_code = json_rsp['payload']['status_code']
        time = round(json_rsp['payload']['time'], 2)
        message = f"{location}:" \
                  f"\n{HTTP_EMOJI.get(status_code//100, '')} {status_code}, ⏰ {time} сек."
    if status == ResponseStatus.ERROR:
        message = json_rsp['payload']['message']
        message = f"{location}: " \
                  f"\n❌ {message}"
    return message


async def send_check_requests(host: str, port: int):
    for node in nodes:
        async with AsyncClient() as client:
            result = await client.get(
                f"{node.address}/http", params=dict(
                    target=host,
                    port=port,
                    token=node.token
                )
            )
        yield result


async def check_web(message: Message, host: str, port: Optional[int]):
    if port is None:
        port = 80
    rsp_msg = await message.answer(f"Отчет о проверке хоста:"
                                   f"\n\n— Хост: {host}:{port}"
                                   f"\n— Дата проверки: {datetime.now():%d.%m.%y в %H:%M} (MSK)"  # TODO: Get timezone
                                   )
    iter_keys = 1  # because I can't use enumerate
    # using generators for magic...
    async for res in send_check_requests(host, port):
        # set typing status...
        await message.bot.send_chat_action(message.chat.id, 'typing')

        node_formatted_response = await prepare_webcheck_message(res)
        rsp_msg = await rsp_msg.edit_text(rsp_msg.text + f"\n\n{iter_keys}. {node_formatted_response}")
        iter_keys = iter_keys + 1
    await rsp_msg.edit_text(rsp_msg.text + f"\n\nПроверка завершена❗")


async def web_cmd(msg: Message):

    port = None
    # TODO: Maybe check it in separated function?
    args = msg.text.split(" ")
    if len(args) < 2:
        return await msg.answer(web_help_message, parse_mode="Markdown")
    if len(args) == 3:
        port = args[2]
        if not check_int(port):
            return await msg.answer(invalid_port, parse_mode="Markdown")
    host = args[1]

    await check_web(msg, host, port)

