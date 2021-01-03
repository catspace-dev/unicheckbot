from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import handlers

storage = MemoryStorage()
telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(telegram_bot, storage=storage)


def on_startup():
	handlers.default.setup(dp)


if __name__ == '__main__':
	on_startup()
	executor.start_polling(dp, skip_updates=True)
