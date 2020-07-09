from conjugate_1 import conjugate_1
from conjugate_2 import conjugate_2
from functions import *
from constants import *
from objects.Entity import Entity
from objects.Time import Time
from objects.Verbs import ConjugatedVerb, InfinitiveVerb


class VerbDictionnary:
    groupes: dict
    terms: dict

    def __init__(self, groupes, terms):
        self.groupes = groupes
        self.terms = terms

    @property
    def verbes(self):
        for verbes in self.groupes.values():
            for verbe in verbes:
                yield verbe

    def verb2group(self, verbe: str) -> int:
        """Pour un verbe infinitif donnée, renvoie son groupe (1, 2, ou 3)"""
        for groupe, verbes in self.groupes.items():
            if verbe in verbes:
                return groupe
        else:
            cws = close_words(verbe, sum(map(list, self.groupes.values()), []), 0.75)
            # raise Exception(f"Le verbe ne correspond à aucune règle de conjugaison ! {', '.join(map(str, cws))}")
            raise Exception(f"Le verbe {verbe} est inconnu du dictionnaire. {', '.join(map(str, cws))}")

    def group2verbs(self, groupe: int) -> list:
        """Pour un groupe donné, renvoie la liste des verbes infinitifs de ce groupe"""
        if groupe in self.groupes:
            return self.groupes[groupe]
        else:
            raise Exception(
                f"Le groupe {groupe} est inconnu, veuillez rentrer une valeur correcte ({', '.join(map(str, self.groupes))})")

    def conjugate(self, verbe: str, timecode: str, entitycode: str = '') -> (list, dict):
        """
            Pour un verbe infinitif donné, renvoie la/les conjugaison(s) de ce verbe en fonction des indications
            timecode : code de temps de la conjugaison recherchée
            entitycode : code d'entité de la conjugaison recherchée
                -> (si absent renvoie la conjugaison pour toutes les personnes du temps)
        """
        groupe = self.verb2group(verbe)

        if groupe in (1, 2):
            method = {1: conjugate_1, 2: conjugate_2}[groupe]
            if entitycode:
                terminaison = self.terms[groupe][timecode][entitycode]
                result = []
                for word in method(verbe, entitycode, timecode, terminaison):
                    result.append(
                        ConjugatedVerb(word, InfinitiveVerb(verbe, groupe), Time(timecode), Entity(entitycode)))
                return result
                # return list(method(verbe, entitycode, timecode, self.terms[groupe][timecode][entitycode]))
            else:
                return dict((entitycode, list(method(verbe, entitycode, timecode, terminaison))) for
                            entitycode, terminaison in
                            self.terms[groupe][timecode].items())
        elif groupe == 3:
            if verbe in self.terms:
                if timecode in self.terms[verbe]:
                    if entitycode:
                        result = []
                        for word in self.terms[verbe][timecode][entitycode]:
                            result.append(
                                ConjugatedVerb(word, InfinitiveVerb(verbe, groupe), Time(timecode), Entity(entitycode)))
                        return result
                    else:
                        return self.terms[verbe][timecode]
                else:
                    raise Exception(
                        f"[TIMECODE] --- La conjugaison pour le verbe ``{verbe}`` au temps ``{timecode}`` est inconnue.")
            else:
                raise Exception(f"[VERBE   ] --- La conjugaison pour le verbe ``{verbe}`` est inconnue.")
        else:
            raise Exception(f"[GROUPE  ] --- Le groupe {groupe} est inconnu.")

    @classmethod
    def fromDir(cls, dirpath: str):
        """Crée un VerbDictionnary à partir d'un dossier valide"""
        assert os.path.exists(dirpath), "directory should exists"
        groupes = {
            1: read_word_file(f'{dirpath}\\infinitifs\\1.txt'),
            2: read_word_file(f'{dirpath}\\infinitifs\\2.txt'),
            3: read_word_file(f'{dirpath}\\infinitifs\\3.txt')
        }
        terms = {
            1: read_conj_file(f'{dirpath}\\conjugaisons\\1.csv'),
            2: read_conj_file(f'{dirpath}\\conjugaisons\\2.csv')
        }
        for filename in os.listdir(f'{dirpath}\\conjugaisons'):
            if filename.endswith('.csv') and filename not in ('1.csv', '2.csv'):
                verbe = filename.split('.')[0]
                conj = read_conj_file(f'{dirpath}\\conjugaisons\\{filename}', full=True)
                if conj.keys():
                    terms[verbe] = conj
        return cls(groupes, terms)

    def toDir(self, dirpath: str):
        """Crée un dossier pour stocker les informations du dictionnaire"""
        assert not os.path.exists(dirpath), "directory shouldn't exists"
        os.makedirs(f'{dirpath}\\conjugaisons')
        os.makedirs(f'{dirpath}\\infinitifs')
        for groupe, data in D.terms.items():
            write_conj_file(f'{dirpath}\\conjugaisons\\{groupe}.csv', data)

        for groupe, data in D.groupes.items():
            write_word_file(f'{dirpath}\\infinitifs\\{groupe}.csv', data)

    def toXMLFile(self, filepath: str):
        """
            Exporte le dictionnaire au format xml
            /!\ attention cette opération peut être longue et crée un fichier massif (+ de 14 MB)
        """
        assert not os.path.exists(filepath)
        assert filepath.endswith('.xml')
        from bs4 import BeautifulSoup

        xml = BeautifulSoup(features="html.parser")
        xml_dict = xml.new_tag("dict")
        xml.append(xml_dict)

        for groupe in self.groupes:
            for verbe in self.group2verbs(groupe):
                xml_verb = xml.new_tag("verbe", infinitif=verbe, groupe=groupe)
                xml_dict.append(xml_verb)

                for timecode in Time.timecodes():
                    xml_conj = xml.new_tag("conj", timecode=timecode)
                    try:
                        for entity, words in self.conjugate(verbe, timecode).items():
                            xml_unit = xml.new_tag("unit", entity=entity)
                            xml_conj.append(xml_unit)
                            xml_unit.string = ",".join(words)
                        xml_verb.append(xml_conj)
                    except:
                        pass

        with open(filepath, mode='w', encoding='utf-8') as file:
            file.write(str(xml))

    def toCSV(self, infinitives: str, conjugated: str) -> None:
        """
        Exporte le dictionnaire de verbe sous la form d'un fichier csv
        :param infinitives: Le chemin du fichier pour les infinitifs
        :param conjugated: Le chemin du fichier pour les conjugaisons
        :return: None
        """
        if not infinitives.endswith('.csv'):
            infinitives += '.csv'
        assert not os.path.exists(infinitives)
        if not conjugated.endswith('.csv'):
            conjugated += '.csv'
        assert not os.path.exists(conjugated)
        with open(infinitives, mode='w', encoding='utf-8') as file_infinitives:
            with open(conjugated, mode='w', encoding='utf-8') as file_conjugated:
                file_conjugated.write(f'forme, groupe, verbe, timecode, entitycode')
                file_infinitives.write(f'verbe, groupe')
                for groupe in self.groupes:
                    for verbe in self.group2verbs(groupe):
                        file_infinitives.write(f'\n{verbe}, {groupe}')
                        for timecode in TIMECODES:
                            try:
                                conj = self.conjugate(verbe, timecode)
                            except:
                                conj = {}
                            for entitycode, formes in conj.items():
                                for forme in formes:
                                    file_conjugated.write(f'\n{forme}, {groupe}, {verbe}, {timecode}, {entitycode}')


def mise_en_forme(data):
    pronoms = {
        '1S': 'je',
        '1S_': "j'",
        '2S': 'tu',
        '3S': 'il/elle',
        '3SM': 'il est',
        '3SF': 'elle est',
        '1P': 'nous',
        '2P': 'vous',
        '3P': 'ils/elles',
        '3PM': 'ils sont',
        '3PF': 'elles sont'
    }
    return '\n'.join(
        f"    {pronoms[key + '_'] if key == '1S' and val[0][0] in 'aeiouy' else pronoms[key]} {' | '.join(val)}" for
        key, val in data.items())


if __name__ == '__main__':
    D = VerbDictionnary.fromDir('assets\\verbes')

    # # affiche les conjugaisons manquantes (verbes ou temps) pour les verbes du 3ème groupe
    # import sys
    # for verbe in D.group2verbs(3):
    #     for timecode in Time.timecodes():
    #         try:
    #             r = D.conjugate(verbe, timecode)
    #         except Exception as e:
    #             print(e, file=sys.stderr)

    # # génère un fichier xml représentatif du dictionnaire (génère toutes les conjugaisons faisables)
    # D.toXMLFile('verb_dict.xml')

    # # compte le temps pris pour conjuguer tous les verbes du groupe 1 et 2 à tous les temps et toutes les personnes
    # import time
    # ti = time.time()
    # for verbe in D.verbes:
    #     if D.verb2group(verbe) in (1, 2):
    #         for timecode in Time.timecodes():
    #             try:
    #                 D.conjugate(verbe, timecode)
    #             except:
    #                 pass
    # tf = time.time()
    # print(tf - ti)

    # # vérifie le mappage (groupe <-> verbes) fonctionne bien
    # for groupe in D.groupes:
    #     for verbe in D.group2verbs(groupe):
    #         _groupe = D.verb2group(verbe)
    #         assert _groupe == groupe, (_groupe, groupe)

    # # conjugue le verbe 'accourcir' à tout les temps
    # for timecode in Time.timecodes():
    #     try:
    #         conj = D.conjugate("manger", timecode)
    #         print(Time(timecode).verbose())
    #         print(mise_en_forme(conj))
    #     except:
    #         pass
    # # affiche la liste des verbes du deuxième groupe
    # print(D.group2verbs(2))

    # # conjugue tous les verbes du deuxième groupe
    # for groupe in D.groupes:
    #     if groupe in [2]:
    #         for verbe in D.group2verbs(groupe):
    #             print(verbe)
    #             for timecode in Time.timecodes():
    #                 print('  '+timecode)
    #                 print(mise_en_forme(D.conjugaisons(verbe, timecode)))

    # # affiche pour la conjugaison de 'manger' au participe passé
    # # version brute / formatée
    # print(D.conjugate("manger", T_PARTICIPE_PASSE))
    # print(mise_en_forme(D.conjugate("manger", T_PARTICIPE_PASSE)))

    # # affiche pour la conjugaison de 'manger' au présent de l'indicatif à la première personne du singulier
    # # version brute / formatée
    # print(D.conjugate("sonder", T_INDICATIF_PRESENT, E1S))
    # print(mise_en_forme(D.conjugate("manger", T_PARTICIPE_PASSE)))
