from .. import (
    core as c,
    utils as ut,
    ctrlstru as cs,
)


class PoolEntry(c.EUDStruct):
    pass

PoolEntry._fields_ = [
    ('prev', PoolEntry),
    ('next', PoolEntry),
    ('value', PoolEntry),
]


class ObjPool(c.EUDStruct):
    _fields_ = [
        ('_emptyhead', PoolEntry),
        ('_usedhead', PoolEntry),
    ]

    def __init__(self, size, basetype=None):
        if basetype is None:
            super().__init__(size)
            return

        # Create entries
        emptysize = size + 1
        entrylist = [c.Forward() for _ in range(emptysize)]
        entryprev = [entrylist[i - 1] for i in range(emptysize)]
        entrynext = [entrylist[(i + 1) % emptysize] for i in range(emptysize)]
        entryvalue = [0] + [basetype() for _ in range(emptysize)]

        for i in range(emptysize):
            entrylist[i] << PoolEntry([
                entryprev[i],
                entrynext[i],
                entryvalue[i]
            ])

        emptyhead = entrylist[0]

        usedhead = c.Forward()
        usedhead << PoolEntry([usedhead, usedhead, 0])

        super().__init__([
            emptyhead,
            usedhead
        ])

    def useditems(self):
        """ Iterator through used items """
        usedhead = self._usedhead
        ptr = usedhead.next
        if cs.EUDWhileNot()(ptr == usedhead):
            yield ptr
            ptr << ptr.next
        cs.EUDEndWhile()

    def alloc(self):
        """ Allocate one object from pool """

        # Pop one from empty list
        emptyhead = self._emptyhead
        ptr = emptyhead.next.asVariable()
        if cs.EUDIfNot()(ptr == emptyhead):
            ptr.next.prev = ptr.prev.next
            ptr.prev.next = ptr.next.prev

            # Put to used list
            usedhead = self._usedhead
            ptr.prev = usedhead.prev
            ptr.next = usedhead.next
            usedhead.prev.next = ptr
            usedhead.prev = ptr
        if cs.EUDElse()():
            ptr << 0
        cs.EUDEndIf()

        return ptr

    def free(self, entry):
        # Remove from used list
        entry.next.prev = entry.prev
        entry.prev.next = entry.next

        # Add to empty list
        emptyhead = self._emptyhead
        entry.next = emptyhead.next
        entry.prev = emptyhead
        emptyhead.next.prev = entry
        emptyhead.next = entry

    def clone(self):
        raise RuntimeError('Pool is not clonable')

    def deepcopy(self):
        raise RuntimeError('Pool is not copyable')
