from assist_bot.config import owner_name


def split(text: str) -> list:
    """
    >>> split('А, б в г, д е ж, два з, четыре к, один н и сто грамм оо ( ля ля ля или ля)')
    ['а', 'б в г', 'д е ж', '2 з', '4 к', '1 н', '100 грамм оо ( ля ля ля или ля)']
    >>> split('А\\nб в г')
    ['а', 'б в г']
    """
    separators = ['. ', ', ', ' и ', '\n']
    result = [text.lower()]
    for separator in separators:
        next_stage = []
        for item in result:
            next_stage.extend(item.split(separator))
        result = next_stage
    return [_numberify(w).rstrip('.').strip() for w in result if w != owner_name]


def _numberify(text: str) -> str:
    """
    >>> _numberify("четыре огурца")
    '4 огурца'
    >>> _numberify("пятьдесят огурцов")
    '50 огурцов'
    >>> _numberify("две банки")
    '2 банки'
    >>> _numberify("триста грамм")
    '300 грамм'
    """
    words = set(text.split(' '))

    for word in words:
        if replace := translations.get(word):
            text = text.replace(word, replace)
    return text


def _make_translations():
    _translations = {
        'один': '1',
        'два': '2',
        'три': '3',
        'четыре': '4',
        'пять': '5',
        'шесть': '6',
        'семь': '7',
        'восемь': '8',
        'девять': '9',
    }
    additionals = dict()
    for key, value in _translations.items():
        if value == 10:
            continue
        if int(value) >= 5:
            additionals[key + 'десят'] = value + '0'
            additionals[key + 'сот'] = value + '00'
        if value in ('2', '3'):
            additionals[key + 'дцать'] = value + '0'
        if value in ('3', '4'):
            additionals[key + 'ста'] = value + '00'
        if value != 2:
            additionals[key.rstrip('ь').rstrip('е') + 'надцать'] = '1' + value
    additionals['десять'] = '10'
    additionals['двенадцать'] = '12'
    additionals['четырнадцать'] = '14'
    additionals['сорок'] = '40'
    additionals['сто'] = '100'
    additionals['двести'] = '200'
    additionals['две'] = '2'
    additionals['одну'] = '1'
    _translations.update(additionals)
    return _translations


translations = _make_translations()
