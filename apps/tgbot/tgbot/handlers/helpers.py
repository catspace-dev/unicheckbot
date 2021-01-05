from httpx import AsyncClient, Timeout, Response, ConnectError, ReadTimeout
from typing import List
from core.coretypes import APINode
from ipaddress import ip_address
from contextlib import suppress
from loguru import logger
from aiogram.bot import Bot
from tgbot.handlers.metrics import push_api_request_status
from tgbot.config import NOTIFICATION_BOT_TOKEN, NOTIFICATION_USERS
from traceback import format_exc


def check_int(value) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def validate_local(target: str) -> bool:
    """
    Validates ip or FQDN is localhost

    :return True if localhost find
    """
    if target == "localhost":
        return True
    with suppress(ValueError):
        ip_addr = ip_address(target)
        if any(
                [ip_addr.is_loopback,
                 ip_addr.is_private,
                 ip_addr.is_multicast,
                 ip_addr.is_link_local,
                 ip_addr.is_unspecified]
        ):
            return True
    return False


async def send_api_requests(endpoint: str, data: dict, nodes: List[APINode]):
    for node in nodes:
        data.update(dict(token=node.token))
        try:
            async with AsyncClient(timeout=Timeout(timeout=100.0)) as client:
                result = await client.get(
                    f"{node.address}/{endpoint}", params=data
                )
        except Exception as e:
            logger.error(f"Node {node.address} got Error. Full exception: {e}")
            # We yield 500 response when get error
            result = Response(500)
            await send_message_to_admins(f"Node {node.address} got error {e}. Full exception: ```{format_exc()}```")
        await push_api_request_status(
            result.status_code,
            endpoint
        )
        yield result


async def send_message_to_admins(message: str):
    bot = Bot(token=NOTIFICATION_BOT_TOKEN)
    for user in NOTIFICATION_USERS:
        logger.info(f"Sended notification to {user}")
        await bot.send_message(user, message, parse_mode='Markdown')
