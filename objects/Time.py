class Time:
    """
        Classification found at : http://www.conjuguetamere.com/temps-conjugaison
        Codes have been extracted from this classification
        > mood : 3 letter code
        > tense : 2 lette code
        full code example : 'IND-PR'

        IND : INDicatif
            PR : PRésent
            PC : Passé Composé
            IM : IMparfait
            PP : Plus-que-Parfait
            PS : Passé Simple
            PA : Passé Antérieur
            FS : Futur Simple
            FA : Futur Antérieur
        SUB : SUBjonctif
            PR : PRésent
            PA : PAssé
            IM : IMparfait
            PP : Plus-que-Parfait
        CON : CONditionnel
            PR : PRésent
            P1 : PAssé (1ère forme)
            P2 : PAssé (2ème forme)
        IMP : IMPératif
            PR : PRésent
            PA : PAssé
        PAR : PARticipe
            PR : PRésent
            PA : PAssé
        INF : INFinitif
            PR : PRésent
            PA : PAssé
        GER : GERondif
            PR : PRésent
            PA : PAssé
    """
    classes = {
        'IND': ('PR', 'PC', 'IM', 'PP', 'PS', 'PA', 'FS', 'FA'),
        'SUB': ('PR', 'PA', 'IM', 'PP'),
        'CON': ('PR', 'P1', 'P2'),
        'IMP': ('PR', 'PA'),
        'PAR': ('PR', 'PA'),
        'INF': ('PR', 'PA'),
        'GER': ('PR', 'PA')
    }

    def __init__(self, code):
        mood, tense = code.split('-')
        assert mood in Time.classes
        assert tense in Time.classes[mood]
        self.mood = mood
        self.tense = tense

    def __hash__(self):
        return self.code.__hash__()

    @property
    def code(self):
        return f"{self.mood}-{self.tense}"

    @property
    def entitycodes(self):
        """Return the conjugate entities allowed in this time"""
        if self.mood == 'GER':
            return '3S',
        elif self.mood == 'INF':
            return '',
        elif self.mood == 'PAR':
            if self.tense == 'PR':
                return '3S',
            elif self.tense == 'PA':
                return '3SM', '3SF', '3PM', '3PF'
            else:
                raise Exception
        else:
            return '1S', '2S', '3S', '1P', '2P', '3P'


# Table de conversion de l'ancien format de temps vers le nouveau (cf. Time)
convert_timecode = {
    'indicatif présent': 'IND-PR',
    'indicatif imparfait': 'IND-IM',
    'indicatif futur simple': 'IND-FS',
    'indicatif passé simple': 'IND-PS',
    'subjonctif présent': 'SUB-PR',
    'subjonctif imparfait': 'SUB-IM',
    'conditionnel présent': 'CON-PR',
    'impératif présent': 'IMP-PR',
    'participe présent': 'PAR-PR',
    'participe passé': 'PAR-PA'
}
