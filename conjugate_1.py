from functions import endswith, est_atone, est_muette, startswith


def conjugate_1(verbe, _entitycode, _timecode, terminaison):
    """
        Règles de conjugaisons issues de :
        ==> https://fr.wikipedia.org/wiki/Conjugaison_des_verbes_du_premier_groupe
    """
    if endswith(verbe, 'yer'):
        if endswith(verbe, 'oyer', 'uyer'):
            if est_atone(terminaison):
                yield verbe[:-3] + 'i' + terminaison
            else:
                yield verbe[:-2] + terminaison
        elif endswith(verbe, 'ayer'):
            if est_atone(terminaison):
                yield verbe[:-3] + 'i' + terminaison
            yield verbe[:-2] + terminaison
        elif endswith(verbe, 'eyer'):
            yield verbe[:-2] + terminaison
        else:
            raise Exception(f"Le verbe ne correspond à aucune règle de conjugaison !")
    elif endswith(verbe, 'guer'):
        yield verbe[:-2] + terminaison
    elif endswith(verbe, 'eler', 'eter'):
        if est_muette(terminaison):
            yield verbe[:-2] + verbe[-3] + terminaison
        else:
            yield verbe[:-2] + terminaison
    elif endswith(verbe, 'evrer', 'ecer', 'eder', 'eger', 'emer', 'ener', 'eper', 'erer', 'eser', 'ever'):
        if est_muette(terminaison):
            if endswith(verbe, 'evrer'):
                yield verbe[:-5] + 'è' + verbe[-4:-2] + terminaison
            else:
                yield verbe[:-4] + 'è' + verbe[-3:-2] + terminaison
        else:
            yield verbe[:-2] + terminaison
    elif endswith(verbe, 'ébrer', 'écher', 'écrer', 'éfler', 'égner', 'égrer', 'éguer', 'équer', 'étrer', 'évrer'):
        if est_atone(terminaison):
            yield verbe[:-5] + 'è' + verbe[-4:-2] + terminaison
        else:
            yield verbe[:-2] + terminaison
    elif endswith(verbe, 'éber', 'écer', 'éder', 'éger', 'éjer', 'éler', 'émer', 'éner', 'éper', 'érer', 'éser',
                  'éter', 'éver'):
        if est_atone(terminaison):
            yield verbe[:-5] + 'è' + verbe[-4:-2] + terminaison
        else:
            yield verbe[:-2] + terminaison
    elif endswith(verbe, 'cer', 'ger'):
        if startswith(terminaison, 'a', 'o'):
            if endswith(verbe, 'cer'):
                yield verbe[:-3] + 'ç' + terminaison
            elif endswith(verbe, 'ger'):
                yield verbe[:-3] + 'ge' + terminaison
            else:
                raise Exception
        else:
            yield verbe[:-2] + terminaison
    else:
        yield verbe[:-2] + terminaison
