import re

from assist_bot import config


IGNORE = {
    'пожалуйста',
    'если есть',
    'плиз'
}


def markdown_checklist_lookup(t: str, query: list[str]) -> str:
    """
    >>> markdown_checklist_lookup('# А\\n## Б\\n- Привет', ['# А', '## Б'])
    '- Привет'
    >>> markdown_checklist_lookup('# А\\n## Б\\n- Привет\\n# В\\n- [x] Куку', ['# В'])
    '- [x] Куку'
    >>> markdown_checklist_lookup('# А\\n## Б\\n- Привет', ['# X'])
    ''
    >>> markdown_checklist_lookup('# А\\n## Б\\n- Привет', ['# А'])
    '- Привет'
    >>> markdown_checklist_lookup('# А\\n## Б\\n- [ ] Привет\\n## Д\\n- [ ] Работает\\n# В\\n- [x] Куку', ['# А'])
    '- [ ] Привет\\n- [ ] Работает'
    """
    depth, path, result = 0, [], []

    for line in t.splitlines():
        if line.startswith('#'):
            line_depth = line.count('#')

            if line_depth > depth:
                path.append(line)
                depth += 1
                continue

            if line_depth < depth:
                path.pop()
                depth -= 1

            path[-1] = line

        elif path[:len(query)] == query:
            result.append(line)

    return '\n'.join(result)


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

    final_result = [_numberify(w) for w in result if w != config.OWNER_NAME if w not in IGNORE]
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
    additional = dict()
    for key, value in _translations.items():
        if value == 10:
            continue
        if int(value) >= 5:
            additional[key + 'десят'] = value + '0'
            additional[key + 'сот'] = value + '00'
        if value in ('2', '3'):
            additional[key + 'дцать'] = value + '0'
        if value in ('3', '4'):
            additional[key + 'ста'] = value + '00'
        if value != 2:
            additional[key.rstrip('ь').rstrip('е') + 'надцать'] = '1' + value
    additional['десять'] = '10'
    additional['двенадцать'] = '12'
    additional['четырнадцать'] = '14'
    additional['сорок'] = '40'
    additional['сто'] = '100'
    additional['двести'] = '200'
    additional['две'] = '2'
    additional['одну'] = '1'
    _translations.update(additional)
    return _translations


translations = _make_translations()
