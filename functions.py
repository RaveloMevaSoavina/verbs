import os
import difflib
import re

from objects.Verbs import ConjugatedVerb


def read_word_file(filepath: str):
    assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.endswith('.txt'), filepath
    with open(filepath, mode='r', encoding='utf-8') as file:
        return list(filter(len, map(str.strip, file.readlines())))


def write_word_file(filepath: str, data: dict):
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write('\n'.join(map(str.strip, data)))


def write_conj_file(filepath: str, data: dict):
    entitycodes = ['timecode', ConjugatedVerb.entitycodes]
    rows = [dict(timecode=timecode, **sdata) for timecode, sdata in data.items()]
    write_csv(filepath, keys=entitycodes, rows=rows)


def read_conj_file(filepath: str, full: bool = False):
    result = {}
    for row in read_csv(filepath, asDict=True):
        if len(row.keys()):
            timecode = row.pop('timecode')
            todelete = [key for key, val in row.items() if val is None]
            for key in todelete:
                del row[key]
            result[timecode] = row
    return result


def endswith(string: str, *ends):
    return any(map(string.endswith, ends))


def startswith(string: str, *starts):
    return any(map(string.startswith, starts))


def est_atone(terminaison: str):
    return terminaison in ('e', 'es')


def est_muette(terminaison: str):
    return terminaison in ('e', 'es')


def close_words(text: str, aliases, threshold: float = 0.75):
    assert 0 <= threshold <= 1
    for alias in aliases:
        sequence = difflib.SequenceMatcher(isjunk=None, a=text, b=alias)
        if sequence.ratio() >= threshold:
            yield alias, sequence.ratio()


def indent(s: str, i: str = '    '):
    return '\n'.join(i + l for l in s.split('\n'))


def write_csv(filepath: str, keys, rows):
    assert isinstance(filepath, str)
    if not filepath.endswith('.csv'):
        filepath += '.csv'

    headline = ','.join(map(str, keys))

    bodylines = [','.join(str(row.get(key, '')) for key in keys) for row in rows]

    content = '\n'.join((headline, *bodylines))

    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write(content)


def read_csv(filepath: str, asDict=False, doInt=True):
    assert isinstance(filepath, str)
    if not filepath.endswith('.csv'):
        filepath += '.csv'

    assert os.path.exists(filepath), filepath
    with open(filepath, mode='r', encoding='utf-8') as file:
        content = ''.join(file.readlines())

    def readline(line, doInt):
        items = list(map(str.strip, line.split(',')))
        for item in items:
            if not item:
                yield None
            elif doInt and re.match('^[0-9]+$', item):
                yield int(item)
            else:
                yield item

    headline, *bodylines = content.split('\n')

    keys = tuple(readline(headline, False))

    for bodyline in bodylines:
        values = readline(bodyline, doInt)
        if asDict:
            yield dict(zip(keys, values))
        else:
            yield list(values)
