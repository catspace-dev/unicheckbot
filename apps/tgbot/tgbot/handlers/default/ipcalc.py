from aiogram.types import Message
from typing import Union
import ipaddress

from tgbot.handlers.base import SimpleCommandHandler, NotEnoughArgs
from tgbot.middlewares.throttling import rate_limit

ipcalc_help_message = """
❓ Калькулятор IP подсетей.

Использование:
 `/ipcalc <ip_with_mask>` 
 `/ipcalc <ip>` - автоматически выставит маску 32
"""


class IPCalcCommandHandler(SimpleCommandHandler):

    help_message = ipcalc_help_message

    def __init__(self):
        super().__init__()

    @rate_limit
    async def handler(self, message: Message):
        try:
            args = self.process_args(message.text)
            network = ipaddress.ip_network(args[1], False)
        except NotEnoughArgs:
            await message.answer(self.help_message, parse_mode='Markdown')
        except ValueError:
            await message.answer(self.help_message, parse_mode='Markdown')
        else:
            msg = await self.prepare_message(network)
            await message.answer(msg)

    def process_args(self, text: str) -> list:
        args = text.split()
        if len(args) == 1:
            raise NotEnoughArgs
        return args

    async def prepare_message(self, ip_net: Union[ipaddress.IPv4Network, ipaddress.IPv6Network]) -> str:

        work_adresses = ip_net.num_addresses - 2
        first_ip = "Нет доступных адресов."
        last_ip = first_ip
        if ip_net.num_addresses <= 2:
            work_adresses = 0
        else:
            first_ip = list(ip_net.hosts())[0]
            last_ip = list(ip_net.hosts())[-1]

        return f"📱 IP подсети: {ip_net.with_prefixlen}\n" \
               f"📌 Маска подсети: {ip_net.netmask}\n" \
               f"📌 Обратная маска: {ip_net.hostmask}\n" \
               f"📌 Широковещательный адрес: {ip_net.broadcast_address}\n" \
               f"📌 Доступные адреса: {ip_net.num_addresses}\n" \
               f"📌 Рабочие адреса: {work_adresses}\n\n" \
               f"🔼 IP первого хоста: {first_ip}\n" \
               f"🔽 IP последнего хоста: {last_ip}"
