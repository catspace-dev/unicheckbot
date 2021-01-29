from aiogram.types import Message
from tgbot.middlewares.throttling import rate_limit

start_message = """

Привет, %name%!

Я @UniCheckBot — бот, позволяющий получить различную информацию о сервере или домене.

Могу пропинговать сервер, проверить TCP порты, получить информацию о minecraft-сервере или IP адресе/домене.

Вот список доступных команд:

📌 `/ping <host>` — пропинговать сервер/сайт
📌 `/ipcalc <ip> <mask>` — посчитать подсеть IP-адресов

📌 `/tcp <host> <port>` — проверить TCP-порт

📌 `/web <host>` — проверить сайт по HTTP с возвратом ответа
📌 `/whois <host>` — узнать владельца IP/домена

📌 `/mc <host> <port>` — проверить сервер Minecraft

Полезные ссылки:

🚩 [Этот бот с открытым с исходным кодом](https://github.com/catspace-dev/unicheckbot)
🚩 [Помогите улучшить бота](https://github.com/catspace-dev/unicheckbot/issues), рассказав об ошибках или предложив что-то новое

Разработчик: [kiriharu](http://t.me/kiriharu)
При поддержке: [Mifuru](https://mifuru.ru/) & [SpaceCore.pro](https://spacecore.pro/)

"""


@rate_limit
async def start_cmd(msg: Message):
    await msg.answer(start_message.replace("%name%", msg.from_user.full_name), parse_mode='markdown', disable_web_page_preview=True)
