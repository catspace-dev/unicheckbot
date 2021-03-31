import sentry_sdk
from tgbot import config

if config.SENTRY_DSN:

    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
    )

from asyncio import sleep

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from . import handlers
from .middlewares import (
    LoggingMiddleware, ThrottlingMiddleware, UserMiddleware, WriteCommandMetric
)

storage = MemoryStorage()
telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(telegram_bot, storage=storage)


async def database_init():
    if config.MYSQL_HOST is not None:
        db_url = f"mysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@" \
                 f"{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}"
    else:
        db_url = "sqlite://db.sqlite3"
    try:
        await Tortoise.init(
            db_url=db_url,
            modules={
                'models': ['tgbot.models']
            }
        )
    except DBConnectionError:
        logger.error("Connection to database failed.")
        await sleep(10)
        await database_init()
    await Tortoise.generate_schemas()
    logger.info("Tortoise inited!")


async def on_startup(disp: Dispatcher):
    await database_init()
    handlers.default.setup(disp)
    disp.middleware.setup(ThrottlingMiddleware())
    disp.middleware.setup(WriteCommandMetric())
    disp.middleware.setup(LoggingMiddleware())
    disp.middleware.setup(UserMiddleware())


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
