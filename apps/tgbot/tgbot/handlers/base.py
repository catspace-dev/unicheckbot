from aiogram.types import Message
from typing import Tuple, Any

from tgbot.nodes import nodes as all_nodes
from httpx import Response
from aiogram.bot import Bot
from datetime import datetime
from core.coretypes import APINodeInfo
from .helpers import send_api_requests, check_int

header = "Отчет о проверке хоста:" \
         "\n\n— Хост: {target_fq}"\
         f"\n— Дата проверки: {datetime.now():%d.%m.%y в %H:%M} (MSK)"  # TODO: Get timezone


class NotEnoughArgs(Exception):
    pass


class InvalidPort(Exception):
    pass


class CheckerBaseHandler:
    help_message = "Set help message in class!"
    header_message = header
    api_endpoint = "Set api endpoint in class!"

    def __init__(self):
        pass

    async def handler(self, message: Message):
        """Always should call check at end"""
        raise NotImplemented

    async def check(self, chat_id: int, bot: Bot, data: dict):
        rsp_msg = await bot.send_message(chat_id, header.format(**data))
        iter_keys = 1  # because I can't use enumerate
        # using generators for magic...
        async for res in send_api_requests(self.api_endpoint, data, all_nodes):
            await bot.send_chat_action(chat_id, 'typing')
            if res.status_code == 500:
                rsp_msg = await rsp_msg.edit_text(rsp_msg.text + f"\n\n{iter_keys}. ❌️ Результат операции не доступен.")
            else:
                node_formatted_response = await self.prepare_message(res)
                rsp_msg = await rsp_msg.edit_text(rsp_msg.text + f"\n\n{iter_keys}. {node_formatted_response}")
            iter_keys = iter_keys + 1
        await rsp_msg.edit_text(rsp_msg.text + f"\n\nПроверка завершена❗")

    async def process_args(self, text: str) -> list:
        raise NotImplemented

    async def message_std_vals(self, res: Response) -> Tuple[str, Any]:
        node = APINodeInfo(**res.json().get("node", None))
        message = f"{node.location}:\n"
        status = res.json().get("status", None)
        return message, status

    async def prepare_message(self, res: Response) -> str:
        raise NotImplemented


def process_args_for_host_port(text: str, default_port: int) -> list:
    port = None
    args = text.split(" ")
    if len(args) < 2:
        raise NotEnoughArgs()
    if len(args) == 2:
        port = default_port
    if len(args) == 3:
        port = args[2]
        if not check_int(port):
            raise InvalidPort()
    host = args[1]
    return [host, port]