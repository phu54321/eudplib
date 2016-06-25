from .vararray import EUDVArray
from .eudv import EUDVariable
from ..allocator import ExprProxy

class EUDStruct(ExprProxy):
    def __init__(self, initvar=None):
        basetype = type(self)
        fields = basetype._fields_

        # Fill fielddict
        fielddict = {}
        for index, nametype in enumerate(fields):
            if isinstance(nametype, str):
                fielddict[nametype] = (index, None)
            else:
                fielddict[nametype[0]] = (index, nametype[1])
        self._fielddict = fielddict

        # With initialization
        if initvar is None:
            fieldnum = len(fields)
            super().__init__(EUDVArray(fieldnum))

        else:
            super().__init__(EUDVArray(initvar))

        self._initialized = True

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError as e:
            attrid, attrtype = self._fielddict[name]
            attr = self.get(attrid)
            if attrtype:
                return attrtype(attr)
            else:
                return attr

    def __setattr__(self, name, value):
        if '_initialized' in self.__dict__:
            attrid, _ = self._fielddict[name]
            self.set(attrid, value)
        else:
            self.__dict__[name] = value
