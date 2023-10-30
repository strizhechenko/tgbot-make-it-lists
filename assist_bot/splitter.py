import re

from assist_bot.config import owner_name


IGNORE = {
    'пожалуйста',
    'если есть',
    'плиз'
}


def split(text: str) -> list:
    """
    >>> split('Пожалуйста, А, б в г, д е ж, два з, четыре к, один н и сто грамм оо ( ля ля ля или ля)')
    ['а', 'б в г', 'д е ж', '2 з', '4 к', '1 н', '100 грамм оо ( ля ля ля или ля)']
    >>> split('А\\nб в г')
    ['а', 'б в г']
    >>> split('a\\nb\\nc\\nd,e')
    ['a', 'b', 'c', 'd,e']
    >>> split('a')
    []
    >>> split('- замерить пол для ворот\\n- написать мужику с воротами\\n')
    ['замерить пол для ворот', 'написать мужику с воротами']
    >>> split('- [ ] замерить пол для ворот\\n- [ ] кушот\\n- [x] написать мужику с воротами\\n')
    ['замерить пол для ворот', 'кушот']
    """
    separators = ['. ', ', ', ' и ', '\n']
    result = [text.lower().strip()]

    if result[0].count('\n') > 2:
        separators = ['\n']

    for separator in separators:
        next_stage = []
        for item in result:
            next_stage.extend(item.split(separator))
        result = next_stage

    final_result = [_numberify(w) for w in result if w != owner_name if w not in IGNORE]
    if final_result == [text]:
        return []

    for pattern in (r'^- \[x\] .*$', r'^- \[ \] ', r'^- '):
        final_result = [re.sub(pattern, '', part) for part in final_result]

    final_result = [part for part in final_result if part]

    return final_result


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
    return text.rstrip('.').strip()


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
