from aiogram import Bot
from aiogram.dispatcher import Dispatcher

import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5624300624:AAGg4B28UlyY93cugMe5j9f82woeMq_SV2w', parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)