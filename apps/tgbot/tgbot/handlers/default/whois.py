from typing import Optional

from whois import whois, parser
from aiogram.types import Message
from dataclasses import dataclass
from whois_vu.api import WhoisSource
from whois_vu.errors import IncorrectZone, QueryNotMatchRegexp

from ..whois_zones import ZONES
from ..base import SimpleCommandHandler
from ..errors import NotEnoughArgs, LocalhostForbidden
from ...middlewares.throttling import rate_limit

whois_help_message = """
❓ Вернёт информацию о домене.

 Использование: `/whois <домен>`
"""

no_domain_text = """
❗Не указан домен или указан неверный/несуществующий домен.

Напишите /whois чтобы посмотреть справку.
"""

incorrect_domain = "❗ Домен {domain} не поддерживается в текущей реализации /whois или его попросту не " \
                   "существует.\n\n" \
                   "📌 Если вы считаете что это какая-то ошибка, " \
                   "то вы можете рассказать " \
                   "нам о ней удобным для вас способом. Контакты указаны в /start."


@dataclass
class DomainAttrClass:
    icon: str
    name: str
    attr: str


# DOMAIN_ATTR_CLASSES order matters!
DOMAIN_ATTR_CLASSES = [
    DomainAttrClass("👤", "Регистратор", "registrar"),
    DomainAttrClass("📅", "Дата создания", "creation_date"),
    DomainAttrClass("📅", "Дата окончания", "expiration_date"),
    DomainAttrClass("📖", "Адрес", "address"),
    DomainAttrClass("🏘", "Город", "city"),
    DomainAttrClass("🏘", "Страна", "country"),
    DomainAttrClass("💬", "Имя", "name"),
    DomainAttrClass("💼", "Организация", "org"),
    DomainAttrClass("💬", "Zipcode", "zipcode"),
    DomainAttrClass("✉", "Почта", "emails"),
    DomainAttrClass("📌", "NS", "name_servers"),
    DomainAttrClass("🔐", "DNSSec", "dnssec"),
]


def whois_request(domain: str) -> parser.WhoisEntry:
    domain_info = whois(domain)
    if domain_info.get("domain_name") is None:
        splitted = domain.split(".")
        ws = WhoisSource().get(domain)
        if zone_class := ZONES.get(splitted[-1], None):
            domain_info = zone_class(domain, ws.whois)
        else:
            domain_info = parser.WhoisEntry.load(domain, ws.whois)
    return domain_info


def create_whois_message(domain: str) -> str:
    try:
        domain_info = whois_request(domain)
    except parser.PywhoisError:
        return f"❗ Домен {domain} свободен или не был найден."
    except IncorrectZone:
        return incorrect_domain.format(domain=domain)
    except QueryNotMatchRegexp:
        return incorrect_domain.format(domain=domain)
    domain_name = domain_info.get("domain_name")
    if not domain_name:
        return incorrect_domain.format(domain=domain)
    if isinstance(domain_name, list):
        domain_name = domain_name[0]
    message = f"\n📝 Информация о домене {domain_name.lower()}:"

    for i, domain_attr in enumerate(DOMAIN_ATTR_CLASSES):
        # for pretty printing, DOMAIN_ATTR_CLASSES order matters!
        if i in [2, 10]:
            message += "\n"
        resp = format_domain_item(
            domain_attr.icon, domain_attr.name, domain_info.get(domain_attr.attr)
        )
        if resp:
            message += resp

    return message


def format_domain_item(icon, item_name, items) -> Optional[str]:
    if not items:
        return
    if isinstance(items, list):
        items = map(str, items)  # fix datetime bug
        message = f"\n{icon} {item_name}:\n"
        message += str.join("\n", [f" * <code>{ns}</code>" for ns in list(set(map(str.lower, items)))])
    else:
        message = f"\n{icon} {item_name}: {items}"
    return message


class WhoisCommandHandler(SimpleCommandHandler):
    help_message = whois_help_message

    def __init__(self):
        super().__init__()

    @rate_limit
    async def handler(self, message: Message):
        try:
            args = self.process_args(message.text)
        except NotEnoughArgs:
            await message.answer(no_domain_text, parse_mode='Markdown')
        except LocalhostForbidden:
            await message.answer(self.localhost_forbidden_message, parse_mode='Markdown')
        else:
            await message.answer(create_whois_message(args[0]), parse_mode='html')

    def process_args(self, text: str) -> list:
        args = text.split()
        if len(args) == 1:
            raise NotEnoughArgs
        if len(args) >= 2:
            host = args[1]
            self.validate_target(host)
            return [host]  # only domain name

    async def prepare_message(self) -> str:
        pass
