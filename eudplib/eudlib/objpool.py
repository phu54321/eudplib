from .. import (
    core as c,
    ctrlstru as cs,
)

from .eudarray import EUDArray


class ObjPool(c.EUDStruct):
    _fields_ = [
        ('data', EUDArray),
        'remaining',
        'size'
    ]

    def __init__(self, size, basetype=None):
        objects = [basetype() for _ in range(size)]
        super().__init__([
            EUDArray(objects),
            size,
            size
        ])
        self._basetype = basetype

    def full(self):
        return self.remaining == 0

    @c.EUDMethod
    def _alloc(self):
        """ Allocate one object from pool """
        if cs.EUDIf()(self.full()):
            c.EUDReturn(0)
        cs.EUDEndIf()

        self.remaining -= 1
        data = self.data[self.remaining]

        return data

    def alloc(self):
        data = self._alloc()
        if self._basetype:
            data = self._basetype(data)
        return data

    @c.EUDMethod
    def free(self, data):
        self.data[self.remaining] = data
        self.remaining += 1

    def clone(self):
        raise RuntimeError('Pool is not clonable')

    def deepcopy(self):
        raise RuntimeError('Pool is not copyable')
