import logging

from assist_bot.assist import Assist
from aiogram import executor

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(Assist().dispatcher)
