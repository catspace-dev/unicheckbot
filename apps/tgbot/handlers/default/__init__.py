from aiogram import Dispatcher

from .start import start_cmd

def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
