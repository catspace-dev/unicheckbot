from aiogram.types import Message
import whois

whois_help_message = """
❓ Вернёт информацию о домене.

 Использование: `/whois <домен>`
"""

no_domain_text = """
❗Не указан домен или указан неверный/несуществующий домен.

Напишите /whois чтобы посмотреть справку.
"""


def create_whois_message(domain: str) -> str:
    domain_info = whois.whois(domain)
    if domain_info.get("domain_name") is None:
        return no_domain_text
    message = f"\n📝Имя: {domain_info.get('domain_name')}" \
              f"\n👤Регистратор: {domain_info.get('registrar')}" \
              f"\n📅Дата создания: {domain_info.get('creation_date')}" \
              f"\n📅Дата окончания: {domain_info.get('expiration_date')}" \
              f"\n📌NS: {' '.join(domain_info.get('name_servers'))}"
    return message


async def whois_cmd(msg: Message):
    args = msg.text.split(" ")
    if len(args) == 1:
        return await msg.answer(no_domain_text)
    if len(args) >= 2:
        host = args[1]
        await msg.answer(create_whois_message(host))
