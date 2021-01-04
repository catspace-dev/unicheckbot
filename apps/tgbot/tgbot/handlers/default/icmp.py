from aiogram.types import Message
from tgbot.nodes import nodes as all_nodes
from httpx import AsyncClient, Response
from datetime import datetime
from core.coretypes import ErrorCodes, ErrorPayload, ICMPCheckerResponse, ResponseStatus, APINodeInfo
from ..helpers import send_api_requests

icmp_help_message = """
❓ Производит проверку хоста по протоколу ICMP.

Использование:
 `/icmp <target>` 
"""


async def prepare_icmp_check_result(res: Response):
    node = APINodeInfo(**res.json().get("node", None))
    message = f"{node.location}:\n"
    status = res.json().get("status", None)

    if status == ResponseStatus.OK:
        payload = ICMPCheckerResponse(**res.json().get("payload"))
        message += f"✅ {payload.min_rtt}/{payload.max_rtt}/{payload.avg_rtt} " \
                   f"⬆{payload.packets_sent} ️⬇️{payload.packets_received} Loss: {payload.loss}"
    if status == ResponseStatus.ERROR:
        payload = ErrorPayload(**res.json().get("payload"))
        message += f"❌️ {payload.message}"
    return message


async def check_icmp(msg: Message, target: str):
    rsp_msg = await msg.answer(f"Отчет о проверке хоста:"
                               f"\n\n— Хост: {target}"
                               f"\n— Дата проверки: {datetime.now():%d.%m.%y в %H:%M} (MSK)"  # TODO: Get timezone
                               )
    iter_keys = 1  # because I can't use enumerate
    # using generators for magic...
    async for res in send_api_requests("icmp", dict(target=target), all_nodes):
        await msg.bot.send_chat_action(msg.chat.id, 'typing')
        node_formatted_response = await prepare_icmp_check_result(res)
        rsp_msg = await rsp_msg.edit_text(rsp_msg.text + f"\n\n{iter_keys}. {node_formatted_response}")
        iter_keys = iter_keys + 1
    await rsp_msg.edit_text(rsp_msg.text + f"\n\nПроверка завершена❗")


async def icmp_cmd(msg: Message):
    args = msg.text.split(" ")
    if len(args) == 1:
        return await msg.answer(icmp_help_message, parse_mode="Markdown")
    if len(args) >= 2:
        target = args[1]
        await check_icmp(msg, target)
