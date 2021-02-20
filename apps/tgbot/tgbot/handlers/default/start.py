from aiogram.types import Message
from ...models.user import User
from ...middlewares.throttling import rate_limit
from ...middlewares.userdata import userdata_required

start_message = """

Привет, *%name%*!

Я @UniCheckBot — бот, позволяющий получить краткую сводку о веб-сервисе. Могу пропинговать, проверить порты, получить информацию о Minecraft-сервере, IP или доменном имени.

Вот список доступных команд:

📌 `/ping <host>` — пропинговать сервер/сайт
📌 `/ipcalc <ip> <mask>` — посчитать подсеть IP-адресов

📌 `/tcp <host> <port>` — проверить TCP-порт

📌 `/web <host>` — проверить сайт по HTTP с возвратом ответа
📌 `/whois <host>` — узнать владельца IP/домена

📌 `/mc <host> <port>` — проверить сервер Minecraft

Полезные ссылки:

🚩 [Этот бот с открытым с исходным кодом](https://github.com/catspace-dev/unicheckbot)
🚩 [Помогите улучшить бота](https://github.com/catspace-dev/unicheckbot/issues) или [расскажите об ошибке](https://github.com/catspace-dev/unicheckbot/issues)

Разработчик: [kiriharu](http://t.me/kiriharu)
При поддержке: [Mifuru](https://mifuru.ru/) & [SpaceCore.pro](https://spacecore.pro/)

"""


@userdata_required
@rate_limit
async def start_cmd(msg: Message, user: User):
    await msg.answer(start_message.replace("%name%", msg.from_user.full_name), parse_mode='markdown', disable_web_page_preview=True)
