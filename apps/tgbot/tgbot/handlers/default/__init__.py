from aiogram import Dispatcher

from .start import start_cmd
from .web import web_cmd
from .whois import whois_cmd
from .icmp import icmp_cmd


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(web_cmd, commands=['web', 'http'])
    dp.register_message_handler(whois_cmd, commands=['whois'])
    dp.register_message_handler(icmp_cmd, commands=['icmp'])
