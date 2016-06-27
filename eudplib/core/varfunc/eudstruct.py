from .vararray import EUDVArray
from ...utils import ExprProxy

from . import structarr


class EUDStruct(ExprProxy, metaclass=structarr._EUDStruct_Metaclass):
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
            initvals = []
            for nametype in fields:
                if isinstance(nametype, str):
                    initvals.append(0)
                else:
                    _, attrtype = nametype
                    initvals.append(attrtype())

            super().__init__(EUDVArray(initvals))

        else:
            super().__init__(EUDVArray(initvar))

        self._initialized = True

    def clone(self):
        """ Create struct clone """
        basetype = type(self)
        inst = basetype()
        self.deepcopy(inst)
        return inst

    def deepcopy(self, inst):
        """ Copy struct to other instance """
        basetype = type(self)
        fields = basetype._fields_
        for i, nametype in enumerate(fields):
            if isinstance(nametype, str):
                inst.set(i, self.get(i))
            else:
                _, attrtype = nametype
                attrtype(self.get(i)).deepcopy(attrtype(inst.get(i)))

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            attrid, attrtype = self._fielddict[name]
            attr = self.get(attrid)
            if attrtype:
                return attrtype(attr)
            else:
                return attr

    def __setattr__(self, name, value):
        if '_initialized' in self.__dict__:
            try:
                attrid, _ = self._fielddict[name]
                self.set(attrid, value)
            except KeyError:
                self.__dict__[name] = value
        else:
            self.__dict__[name] = value
