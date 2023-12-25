import json
from pathlib import Path
from aiogram import Bot, Dispatcher, types

from assist_bot import config
from assist_bot.splitter import split


class Assist:
    bot = Bot(token=config.TOKEN)
    dispatcher = Dispatcher(bot=bot)
    _known_file = Path('./known.json')
    known = json.loads(_known_file.read_text(encoding='utf-8')) if _known_file.exists() else dict()

    @staticmethod
    @dispatcher.message_handler()
    async def search(message: types.Message):
        if message.from_user.username == config.OWNER:
            if message.text in Assist.known:
                return await Assist.decompose_known(message)
            for reply in split(message.text):
                await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    async def decompose_known(message):
        for reply in Assist.known[message.text]:
            await Assist.bot.send_message(message.chat.id, reply)
