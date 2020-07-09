import os
import difflib
import re

from constants import ENTITYCODES


def read_word_file(filepath: str):
    assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.endswith('.txt')
    with open(filepath, mode='r', encoding='utf-8') as file:
        return list(filter(len, map(str.strip, file.readlines())))


def write_word_file(filepath: str, data: dict):
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write('\n'.join(map(str.strip, data)))


def write_conj_file(filepath: str, data: dict):
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write(','.join(ENTITYCODES) + '\n')
        file.write('\n'.join(
            timecode + ':' + ','.join(terms.get(entitycode, '') for entitycode in ENTITYCODES) for timecode, terms in
            data.items()))


def read_conj_file(filepath: str, full: bool = False):
    assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.endswith('.txt')
    with open(filepath, mode='r', encoding='utf-8') as file:
        entitycodes = list(map(str.strip, file.readline().strip().split(',')))
        result = {}
        for line in filter(len, map(str.strip, file.readlines())):
            if ':' in line:
                timecode, terms_string = map(str.strip, line.split(':'))
                conjugaison = {}
                terminaisons = map(str.strip, terms_string.split(','))
                for entitycode, terminaison in zip(entitycodes, terminaisons):
                    if terminaison:
                        if full:
                            conjugaison[entitycode] = list(map(str.strip, terminaison.split('/')))
                        else:
                            conjugaison[entitycode] = terminaison
                result[timecode] = conjugaison
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


def load_csv(filepath, asDict=False, doInt=True):
    assert filepath.endswith('.csv') and os.path.exists(filepath)
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

    keys = readline(headline, False)

    for bodyline in bodylines:
        values = readline(bodyline, doInt)
        if asDict:
            yield dict(zip(keys, values))
        else:
            yield list(values)
