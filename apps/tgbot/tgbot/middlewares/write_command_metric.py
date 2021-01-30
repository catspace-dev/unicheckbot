from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from tgbot.handlers.metrics import push_metric
from tgbot.models import User, UserCheckRequests


class WriteCommandMetric(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        # commands to DB
        user, _ = await User.get_or_create(telegram_id=message.from_user.id)
        await UserCheckRequests.create(user=user, request=message.text)

        # metrics to influxdb
        await push_metric(
            measurement="bot_processed_messages",
            fields=dict(
                telegram_id=message.from_user.id,
                full_command=message.text,
                value=1,
            ),
            tags=dict(
                command=message.text.split()[0],
                type="command"
            )
        )
