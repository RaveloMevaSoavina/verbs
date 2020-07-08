import os
import difflib

from constants import ENTITYCODES


def read_word_file(filepath):
    assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.endswith('.txt')
    with open(filepath, mode='r', encoding='utf-8') as file:
        return list(filter(len, map(str.strip, file.readlines())))


def write_word_file(filepath, data):
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write('\n'.join(map(str.strip, data)))


def write_conj_file(filepath, data):
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write(','.join(ENTITYCODES) + '\n')
        file.write('\n'.join(
            timecode + ':' + ','.join(terms.get(entitycode, '') for entitycode in ENTITYCODES) for timecode, terms in
            data.items()))


def read_conj_file(filepath):
    assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.endswith('.txt')
    with open(filepath, mode='r', encoding='utf-8') as file:
        entitycodes = list(map(str.strip, file.readline().strip().split(',')))
        result = {}
        for line in filter(len, map(str.strip, file.readlines())):
            if ':' in line:
                timecode, terms = map(str.strip, line.split(':'))
                result[timecode] = dict(
                    (entitycode, term) for entitycode, term in zip(entitycodes, map(str.strip, terms.split(','))) if
                    term)
        return result


def endswith(string, *ends):
    return any(map(string.endswith, ends))


def startswith(string, *starts):
    return any(map(string.startswith, starts))


def est_atone(terminaison):
    return terminaison in ('e', 'es')


def est_muette(terminaison):
    return terminaison in ('e', 'es')


def close_words(text, aliases, threshold=0.75):
    for alias in aliases:
        sequence = difflib.SequenceMatcher(isjunk=None, a=text, b=alias)
        if sequence.ratio() >= threshold:
            yield alias, sequence.ratio()


def indent(s, i='    '):
    return '\n'.join(i + l for l in s.split('\n'))
