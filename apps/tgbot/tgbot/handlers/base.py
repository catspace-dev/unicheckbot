from datetime import datetime
from time import time
from typing import Any, List, Tuple
from uuid import uuid4

from aiogram.bot import Bot
from aiogram.types import Message
from core.coretypes import APINodeInfo
from httpx import Response
from loguru import logger

from ..middlewares.throttling import rate_limit
from ..nodes import nodes as all_nodes
from .errors import InvalidPort, LocalhostForbidden, NotEnoughArgs
from .helpers import send_api_requests
from .validators import BaseValidator, LocalhostValidator

header = "Отчет о проверке хоста:" \
         "\n\n— Хост: {target_fq}"\
         f"\n— Дата проверки: {datetime.now():%d.%m.%y в %H:%M} (MSK)"  # TODO: Get timezone


class SimpleCommandHandler:
    help_message = "Set help message in class!"
    localhost_forbidden_message = "❗ Локальные адреса запрещены"
    validators: List[BaseValidator] = [LocalhostValidator()]

    @rate_limit
    async def handler(self, message: Message):
        pass

    def process_args(self, text: str) -> list:
        raise NotImplemented

    def validate_target(self, target: str):
        for validator in self.validators:
            validator.validate(target)

    async def prepare_message(self, *args) -> str:
        raise NotImplemented


class CheckerBaseHandler(SimpleCommandHandler):
    invalid_port_message = "Invalid port!"
    header_message = header
    api_endpoint = "Set api endpoint in class!"

    def __init__(self):
        pass

    async def check(self, chat_id: int, bot: Bot, data: dict):
        # TODO: start check and end check metrics with ident, chat_id and api_endpoint
        ts = time()
        ident = uuid4().hex
        logger.info(f"User {chat_id} started check {ident}")
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
        logger.info(f"User {chat_id} ended check {ident}")
        await rsp_msg.edit_text(rsp_msg.text + f"\n\nПроверка завершена❗")
        te = time()
        logger.info(f"func {__name__} took {te - ts} sec")

    async def message_std_vals(self, res: Response) -> Tuple[str, Any]:
        node = APINodeInfo(**res.json().get("node", None))
        message = f"{node.location}:\n"
        status = res.json().get("status", None)
        return message, status


class CheckerTargetPortHandler(CheckerBaseHandler):

    @rate_limit
    async def handler(self, message: Message):
        """This hanler can be used if you need target port args"""
        try:
            args = self.process_args(message.text)
        except NotEnoughArgs:
            logger.info(f"User {message.from_user.id} got NotEnoughArgs error")
            return await message.answer(self.help_message, parse_mode="Markdown")
        except InvalidPort:
            logger.info(f"User {message.from_user.id} got InvalidPort error")
            return await message.answer(self.invalid_port_message, parse_mode="Markdown")
        try:
            self.validate_target(args[0])
        except ValueError:  # For ip check
            pass
        except LocalhostForbidden:
            logger.info(f"User {message.from_user.id} got LocalhostForbidden error")
            return await message.answer(self.localhost_forbidden_message, parse_mode="Markdown")
        await self.check(
            message.chat.id,
            message.bot,
            dict(target=args[0], port=args[1], target_fq=f"{args[0]}:{args[1]}")
        )


def parse_host_port(text: str, default_port: int) -> Tuple[str, int]:
    """Parse host:port
    """
    text = text.strip()
    port = default_port
    host = text
    if ":" in text:
        host, port = text.rsplit(":", 1)
    elif " " in text:
        host, port = text.rsplit(" ", 1)

    try:
        port = int(port)
        # !Important: Don't check range if port == default_port!
        assert port == default_port or port in range(1, 65_536)
    except (ValueError, AssertionError):
        raise InvalidPort(port)
    
    return (host, port)


def process_args_for_host_port(text: str, default_port: int) -> Tuple[str, int]:
    """Parse target from command
    """
    args = text.split(' ', 1)
    if len(args) != 2:
        raise NotEnoughArgs()
    target = args[1]
    return parse_host_port(target, default_port)
