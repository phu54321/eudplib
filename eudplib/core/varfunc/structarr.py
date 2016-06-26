from .vararray import EUDVArray
from ...utils import ExprProxy


class _EUDStruct_Metaclass(type):
    def __mul__(self, times):
        basetype = self

        class EUDStructArray(ExprProxy):
            __metaclass__ = _EUDStruct_Metaclass

            def __init__(self, initvar=None):
                if initvar is None:
                    initvals = [basetype() for _ in range(times)]
                    super().__init__(EUDVArray(initvals, basetype))
                else:
                    super().__init__(EUDVArray(initvar, basetype))

                self._initialized = True

            def clone(self):
                """ Create struct clone """
                arraytype = type(self)
                inst = arraytype()
                self.deepcopy(inst)
                return inst

            def deepcopy(self, inst):
                """ Copy struct to other instance """
                for i in range(times):
                    self[i].deepcopy(inst[i])

            def __getitem__(self, index):
                return self.getValue()[index]

            def __setitem__(self, index, newval):
                self.getValue()[index] = newval

            def __getattr__(self, name):
                return super().__getattr__(name)

            def __setattr__(self, name, value):
                self.__dict__[name] = value

        return EUDStructArray
