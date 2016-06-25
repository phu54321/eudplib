from .vararray import EUDVArray
from ..allocator import EUDObjectView


class EUDStruct(EUDObjectView):
    def __init__(self, initvar=None):
        basetype = type(self)
        fields = basetype._fields_
        self._fielddict = {
            name: index for index, name in enumerate(fields)
        }

        if initvar is None:
            fieldnum = len(fields)
            self._data = EUDVArray(fieldnum)

        else:
            self._data = EUDVArray(initvar)

        super().__init__(self._data)
        self._initialized = True

    def __getattr__(self, name):
        attrid = self._fielddict[name]
        return self._data.get(attrid)

    def __setattr__(self, name, value):
        if '_initialized' in self.__dict__:
            attrid = self._fielddict[name]
            self._data.set(attrid, value)
        else:
            self.__dict__[name] = value
