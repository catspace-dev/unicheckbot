import asyncio
from traceback import format_exc
from typing import List

from aiogram.bot import Bot
from core.coretypes import APINode
from httpx import AsyncClient, Response, Timeout
from loguru import logger
from sentry_sdk import capture_exception

from ..config import NOTIFICATION_BOT_TOKEN, NOTIFICATION_USERS
from .metrics import push_api_request_status


async def send_api_request(client: AsyncClient, endpoint: str, data: dict, node: APINode):
    try:
        data['token'] = node.token
        result = await client.get(
            f"{node.address}/{endpoint}", params=data
        )
    except Exception as e:
        exc_id = capture_exception(e)
        # Remove token from log data
        data.pop('token', None)
        logger.error(f"Node {node.address} got Error. Data: {data}. Endpoint: {endpoint}. Full exception: {e}")
        result = Response(500)
        if exc_id:
            await send_message_to_admins(f"Node {node.address} got error: `{e}`. \n"
                                         f"Data: `{data}`, Endpoint: `{endpoint}`\n"
                                         f"Exc sentry: {exc_id}")
        else:
            await send_message_to_admins(f"Node {node.address} got error: `{e}`. \n"
                                         f"Data: `{data}`, Endpoint: `{endpoint}`\n"
                                         f"Full exception: ```{format_exc()}```")
        await push_api_request_status(
            result.status_code,
            endpoint
        )
    return result


async def send_api_requests(endpoint: str, data: dict, nodes: List[APINode]):
    async with AsyncClient(timeout=Timeout(timeout=100.0)) as client:
        tasks = [send_api_request(client, endpoint, data, node) for node in nodes]
        for completed in asyncio.as_completed(tasks):
            res = await completed
            yield res


async def send_message_to_admins(message: str):
    if NOTIFICATION_BOT_TOKEN:
        bot = Bot(token=NOTIFICATION_BOT_TOKEN)
        for user in NOTIFICATION_USERS:
            logger.info(f"Sended notification to {user}")
            await bot.send_message(user, message, parse_mode='Markdown')
    else:
        logger.warning(f"Notificator bot token not setted. Skipping send notifications to admin")
