from whois import whois, parser
from aiogram.types import Message
from aiogram.utils.markdown import quote_html

from tgbot.handlers.base import SimpleCommandHandler
from tgbot.handlers.errors import NotEnoughArgs, LocalhostForbidden
from tgbot.middlewares.throttling import rate_limit

whois_help_message = """
❓ Вернёт информацию о домене.

 Использование: `/whois <домен>`
"""

no_domain_text = """
❗Не указан домен или указан неверный/несуществующий домен.

Напишите /whois чтобы посмотреть справку.
"""


def create_whois_message(domain: str) -> str:
    try:
        domain_info = whois(domain)
    except parser.PywhoisError as e:
        return f"❗ Домен {domain} свободен или не был найден."
    domain_name = domain_info.get("domain_name")
    if domain_name is None:
        return no_domain_text

    if isinstance(domain_name, list):
        domain_name = domain_name[0]

    message = f"\n📝 Информация о домене {domain_name.lower()}:" \
              f"\n\n👤 Регистратор: {domain_info.get('registrar')}" \

    if creation_date := domain_info.get('creation_date'):
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        message += f"\n📅 Дата создания: {creation_date}"

    if expiration_date := domain_info.get('expiration_date'):
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        message += f"\n📅 Дата окончания:: {expiration_date}\n"

    if address := domain_info.get("address"):
        if isinstance(address, list):
            message += "\n📖 Адрес: \n" + str.join("\n", [f" * <code>{address_obj}</code>" for address_obj in address])
        else:
            message += f"\n📖 Адрес: {address}"
    if city := domain_info.get("city"):
        if isinstance(city, list):
            message += "\n🏘 Город: \n" + str.join("\n", [f" * <code>{city_obj}</code>" for city_obj in city])
        else:
            message += f"\n🏘 Город: {city}"
    if country := domain_info.get("country"):
        message += f"\n🏳️ Страна: {country}"
    if name := domain_info.get("name"):
        if isinstance(name, list):
            message += "\n🏘 💬 Имя: \n" + str.join("\n", [f" * <code>{name_obj}</code>" for name_obj in name])
        else:
            message += f"\n💬 Имя: {name}"
    if org := domain_info.get("org"):
        message += f"\n💼 Организация: {org}"
    if zipcode := domain_info.get("zipcode"):
        message += f"\n🖥 Zipcode: {zipcode}"
    if emails := domain_info.get("emails"):
        message += "\n✉️ Почта: \n" + str.join("\n", [f" * <code>{email}</code>" for email in emails])

    if name_servers := domain_info.get('name_servers'):
        message += "\n\n📌 NS: \n" + str.join("\n", [f" * <code>{ns}</code>" for ns in
                                                     list(set(map(str.lower, name_servers)))])
    if dnssec := domain_info.get("dnssec"):
        message += f"\n🔐 DNSSec: {dnssec}"
    return message


class WhoisCommandHandler(SimpleCommandHandler):

    help_message = whois_help_message

    def __init__(self):
        super().__init__()

    @rate_limit
    async def handler(self, message: Message):
        try:
            args = await self.process_args(message.text)
        except NotEnoughArgs:
            await message.answer(no_domain_text, parse_mode='Markdown')
        except LocalhostForbidden:
            await message.answer(self.localhost_forbidden_message, parse_mode='Markdown')
        else:
            await message.answer(create_whois_message(args[0]), parse_mode='html')

    async def process_args(self, text: str) -> list:
        args = text.split()
        if len(args) == 1:
            raise NotEnoughArgs
        if len(args) >= 2:
            host = args[1]
            await self.validate_target(host)
            return [host]  # only domain name

    async def prepare_message(self) -> str:
        pass
