from aiogram.types import Message
from httpx import Response
from core.coretypes import ErrorPayload, ICMPCheckerResponse, ResponseStatus
from ..base import CheckerBaseHandler, NotEnoughArgs, LocalhostForbidden
from ..metrics import push_status_metric
from ...middlewares.throttling import rate_limit

icmp_help_message = """
❓ Производит проверку хоста по протоколу ICMP.

Использование:
 `/icmp <target>` 
"""


class ICMPCheckerHandler(CheckerBaseHandler):
    help_message = icmp_help_message
    api_endpoint = "icmp"

    def __init__(self):
        super(ICMPCheckerHandler, self).__init__()

    @rate_limit
    async def handler(self, message: Message):
        try:
            args = self.process_args(message.text)
        except NotEnoughArgs:
            return await message.answer(icmp_help_message, parse_mode="Markdown")
        except LocalhostForbidden:
            return await message.answer(self.localhost_forbidden_message, parse_mode="Markdown")
        else:
            await self.check(message.chat.id, message.bot, dict(target=args[0], target_fq=args[0]))

    def process_args(self, text: str) -> list:
        args = text.split()
        if len(args) == 1:
            raise NotEnoughArgs()
        if len(args) >= 2:
            target = args[1]
            self.validate_target(target)
            return [target]

    async def prepare_message(self, res: Response):
        message, status = await self.message_std_vals(res)
        if status == ResponseStatus.OK:
            payload = ICMPCheckerResponse(**res.json().get("payload"))
            message += f"✅ {payload.min_rtt}/{payload.max_rtt}/{payload.avg_rtt} " \
                       f"⬆{payload.packets_sent} ️⬇️{payload.packets_received} Loss: {payload.loss}"
        if status == ResponseStatus.ERROR:
            payload = ErrorPayload(**res.json().get("payload"))
            message += f"❌️ {payload.message}"
        await push_status_metric(status, self.api_endpoint)
        return message
