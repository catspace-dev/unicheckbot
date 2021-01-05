from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from tgbot.handlers.metrics import push_metric


class WriteCommandMetric(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        await push_metric(
            measurement="bot_processed_messages",
            fields=dict(
                telegram_id=message.from_user.id,
                full_command=message.text,
                value=1,
            ),
            tags=dict(
                command=message.text.split(" ")[0],
                type="command"
            )
        )
