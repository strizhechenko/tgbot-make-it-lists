from aiogram import Bot, Dispatcher, types

from assist_bot.config import token, owner
from assist_bot.splitter import split


class Assist:
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot=bot)

    @staticmethod
    @dispatcher.message_handler()
    async def search(message: types.Message):
        if message.from_user.username == owner:
            for reply in split(message.text):
                await Assist.bot.send_message(message.chat.id, reply)
