## Limits

1. Bot only supports russian numeric words.
2. I don't assume it's useful for non-russian speakers.
3. So next parts of README are in russian only, sorry.

## Зачем

Иногда жена или мама пишут мне здоровенный список покупок в телегу. Пересылаем сообщение боту...

**Мама**:

- Если есть желтых помидор, два огурца, четыре банана, один лимон и 100 грамм хорошего сыра

**Бот**:

- если есть желтых помидор
- 2 огурца
- 4 банана
- 1 лимон
- 100 грамм хорошего сыра

И вот эти ответы бота удалять или помечать реакциями, чтобы понять, что осталось купить, куда удобнее чем парсить глазами длиннющее сообщение.

## Почему просто не дать ссылку на моего бота и не разрешить пользоваться им всем?

Мне лень разбираться с законодательством о персональных данных, конфиденциальностью и прочим. Software provided as is.

## Запуск

1. Установите одну единственную зависимость: `pip3 install -r requirements.txt` или `pip install aiogram`.
2. Надо сгенерировать какой-то `./assist_bot/config.py`, пример в `config.py.example`, либо дописать чтение из ENV. В общем, любым способом надо добиться чтобы `from config import owner, owner_name, token` работали.
   - Регистрируем бота у [BotFather](https://t.me/BotFather), получаем `token`. Прописываем его в `config.py`. 
   - Пишем в `owner` свой username (часть ссылки на свой профиль после https://t.me/).
   - Прописываем своё имя в `owner_name`, чтобы обращения по имени не попадали в списки в ответах.
3. `python3 main.py`

## Тут даже тесты есть (2 шт)

``` shell
pytest --doctest-modules
```

## Автозапуск в systemd

``` shell
git clone https://github.com/strizhechenko/tgbot-make-it-lists.git /opt/tgbot/
ln -sf /opt/tgbot/tgbot.service /etc/systemd/system/tgbot.service
systemctl enable --now tgbot.service
systemctl status tgbot.service
```

## Поддержка Docker, k8s

Я не против, поддерживайте.
