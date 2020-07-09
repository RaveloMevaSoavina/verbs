from objects.Entity import Entity
from objects.Time import Time


class InfinitiveVerb:
    instances = {}

    word: str
    group: int

    def __new__(cls, word, group, *_, **__):
        if word in cls.instances:
            return cls.instances[word]
        else:
            instance = object.__new__(cls)
            instance.__init__(word, group)
            return instance

    def __init__(self, word: str, group: int):
        if not hasattr(self, '_lock'):
            assert group in (1, 2, 3)
            if group == 1:
                assert word.endswith('er')
            elif group == 2:
                assert word.endswith('ir') or word.endswith('ïr')
            self.word = word
            self.group = group

            InfinitiveVerb.instances[self.word] = self
            self._lock = True

    def __repr__(self):
        return f"Verb{self.group}({self.word})"


class ConjugatedVerb:
    word: str
    infinitive: InfinitiveVerb
    time: Time
    entity: Entity

    def __init__(self, word: str, infinitive: InfinitiveVerb, time: Time, entity: Entity):
        assert entity.code in time.entitycodes, (time.mood, time.tense, entity.code, time.entitycodes)
        self.word = word
        self.infinitive = infinitive
        self.time = time
        self.entity = entity

    @property
    def group(self):
        return self.infinitive.group

    def __repr__(self):
        return f"Conj({self.word})[{self.infinitive} + {self.time.code}-{self.entity.code}]"





# from functions import load_csv
# if __name__ == '__main__':
#     for word, group in load_csv('../assets/verbes/infinitifs.csv'):
#         verb = InfinitiveVerb(word, group)
#         print(verb)
#
#     for word, group, verb, timecode, entitycode in load_csv('../assets/verbes/conjugués.csv'):
#         verb = InfinitiveVerb(verb, group)
#         time = Time(convert_timecode.get(timecode, timecode))
#         entity = Entity(entitycode)
#         conj = ConjugatedVerb(word, verb, time, entity)
#         print(conj)
