from constants import T_INDICATIF_PRESENT, E1S, E2S, E3S
from functions import endswith


def conjugate_2(verbe, entitycode, timecode, terminaison):
    """
        Règles de conjugaisons issues de :
        ==> https://fr.wikipedia.org/wiki/Conjugaison_des_verbes_du_deuxi%C3%A8me_groupe
    """
    if verbe == 'fleurir':
        yield verbe[:-2] + terminaison
        yield 'flor' + terminaison
    elif verbe == 'haïr' and timecode == T_INDICATIF_PRESENT and entitycode in (E1S, E2S, E3S):
        yield verbe[:-2] + terminaison
    elif endswith(verbe, 'ï'):
        if terminaison[0] == 'i':
            yield verbe[:-1] + terminaison[1:]
        else:
            yield verbe[:-2] + terminaison
    else:
        yield verbe[:-2] + terminaison
