import re


class Entity:
    """
        Definition of the entity code which is used to know the person, number and gender of an entity
    """

    def __init__(self, code):
        assert isinstance(code, str) and re.match('^[123]?[SP]?[MF]?$', code)
        self.code = code
        self.person = 1 if '1' in self.code else 2 if '2' in self.code else 3 if '3' in self.code else '?'
        self.number = 'singular' if 'S' in self.code else 'plural' if 'P' in self.code else '?'
        self.gender = 'male' if 'M' in self.code else 'female' if 'F' in self.code else '?'

    def __hash__(self):
        return self.code.__hash__()

    def __contains__(self, ec):
        if isinstance(ec, str):
            ec = Entity(ec)
        assert isinstance(ec, Entity)
        return all(c in ec.code for c in self.code)
