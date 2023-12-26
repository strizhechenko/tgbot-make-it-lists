import json
import locale
import logging
from datetime import datetime
from pathlib import Path
from aiogram import Bot, Dispatcher, types

from assist_bot import config
from assist_bot.splitter import split, markdown_checklist_lookup


class Assist:
    bot = Bot(token=config.TOKEN)
    dispatcher = Dispatcher()
    _known_file = Path('./known.json')
    _agenda_file = Path('./agenda.md')
    known = json.loads(_known_file.read_text(encoding='utf-8')) if _known_file.exists() else dict()

    @staticmethod
    @dispatcher.message()
    async def search(message: types.Message):
        if message.from_user.username == config.OWNER:
            if message.text in Assist.known:
                return await Assist.decompose_known(message)
            if message.text == 'сегодня':
                return await Assist.today_agenda(message)
            for reply in split(message.text):
                await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    async def decompose_known(message):
        for reply in Assist.known[message.text]:
            await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    async def today_agenda(message):
        if not Assist._agenda_file.exists():
            await Assist.bot.send_message(message.chat.id, "Никаких планов вообще")
            return

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        day_of_week = datetime.now().strftime('%A')
        query = ['# Эта неделя', '## ' + day_of_week]
        text = Assist._agenda_file.read_text(encoding='utf-8')
        result = markdown_checklist_lookup(text, query)
        results = split(result)

        if not results:
            await Assist.bot.send_message(message.chat.id, "Никаких планов")

        for reply in results:
            await Assist.bot.send_message(message.chat.id, reply)
