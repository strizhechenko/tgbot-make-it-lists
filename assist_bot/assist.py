import json
import locale
import logging
import re

from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.utils.formatting import Code
from aiogram.enums import ParseMode

from assist_bot import config
from assist_bot.splitter import split, markdown_checklist_lookup

log = logging.getLogger(__name__)


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
            text = message.text
            if text in Assist.known:
                return await Assist.decompose_known(message)
            for command in ('сегодня', 'завтра', 'послезавтра', 'вчера', 'эта неделя', 'следующая неделя'):
                if re.match(command, text.lower()):
                    do_split = 'пачкой' not in text.lower()
                    return await Assist.agenda(message, do_split)
            for reply in split(message.text):
                await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    async def decompose_known(message):
        for reply in Assist.known[message.text]:
            await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    async def agenda(message, do_split: bool = True):
        if not Assist._agenda_file.exists():
            await Assist.bot.send_message(message.chat.id, "Никаких планов вообще")
            return

        words = ' '.join(filter(lambda x: x != 'пачкой', message.text.lower().split(' ')))
        query = Assist.markdown_query_from(words)
        text = Assist._agenda_file.read_text(encoding='utf-8')
        result = markdown_checklist_lookup(text, query)

        if not result:
            return await Assist.bot.send_message(message.chat.id, "Никаких планов")

        if not do_split:
            return await Assist.bot.send_message(
                message.chat.id, Code(result).as_markdown(), parse_mode=ParseMode.MARKDOWN_V2
            )

        results = split(result)

        if not results:
            return await Assist.bot.send_message(message.chat.id, "Никаких планов")

        for reply in results:
            await Assist.bot.send_message(message.chat.id, reply)

    @staticmethod
    def markdown_query_from(text: str) -> list[str]:
        """
        >>> import freezegun
        >>> with freezegun.freeze_time('2024.01.14'): Assist.markdown_query_from('сегодня')
        ['# Эта неделя', '## Воскресенье']
        >>> with freezegun.freeze_time('2024.01.14'): Assist.markdown_query_from('завтра')
        ['# Следующая неделя', '## Понедельник']
        >>> with freezegun.freeze_time('2024.01.14'): Assist.markdown_query_from('послезавтра')
        ['# Следующая неделя', '## Вторник']
        >>> with freezegun.freeze_time('2024.01.15'): Assist.markdown_query_from('послезавтра')
        ['# Эта неделя', '## Среда']
        >>> with freezegun.freeze_time('2024.01.14'): Assist.markdown_query_from('вчера')
        ['# Эта неделя', '## Суббота']
        """
        if text in ('эта неделя', 'следующая неделя'):
            return ['# ' + text.capitalize()]
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        today = datetime.now()
        day = today + timedelta(days={
            'сегодня': 0,
            'завтра': 1,
            'послезавтра': 2,
            'вчера': -1,
        }.get(text))
        day_of_week = day.strftime('%A')
        week = '# Эта неделя' if today.isoweekday() <= day.isoweekday() or text == 'вчера' else '# Следующая неделя'
        return [week, '## ' + day_of_week]
