# verbs
outil pour la gestion des verbes en français / tool for french verbs handling

class VerbDictionnary
 |  ----------------------------------------------------------------------
 |  Methodes :
 |  ----------------------------------------------------------------------
 |  conjugate(self, verbe: str, timecode: str, entitycode: str = '') -> (<class 'list'>, <class 'dict'>)
 |      Pour un verbe infinitif donné, renvoie la/les conjugaison(s) de ce verbe en fonction des indications
 |      timecode : code de temps de la conjugaison recherchée (voir dans ``constants.py`` les timecodes valides)
 |      entitycode : code d'entité de la conjugaison recherchée (voir dans ``constants.py`` les entitycodes valides)
 |          -> (si absent renvoie la conjugaison pour toutes les personnes du temps)
 |  ----------------------------------------------------------------------
 |  group2verbs(self, groupe: int) -> list
 |      Pour un groupe donné, renvoie la liste des verbes infinitifs de ce groupe
 |  ----------------------------------------------------------------------
 |  toDir(self, dirpath)
 |      Crée un dossier pour stocker les informations du dictionnaire
 |  ----------------------------------------------------------------------
 |  toXMLFile(self, filepath)
 |      Exporte le dictionnaire au format xml
 |      /!\ attention cette opération peut être longue et crée un fichier massif (+ de 14 MB)
 |  ----------------------------------------------------------------------
 |  verb2group(self, verbe: str) -> int
 |      Pour un verbe infinitif donnée, renvoie son groupe (1, 2, ou 3)
 |  ----------------------------------------------------------------------
 |  Methodes de classe :
 |  ----------------------------------------------------------------------
 |  fromDir(dirpath) from builtins.type
 |      Crée un VerbDictionnary à partir d'un dossier valide
