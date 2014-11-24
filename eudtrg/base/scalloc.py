from . import rlocint

_alloctable = {}
_alloc_lastaddr = 0


def ClearAllocTable():
    global _alloctable, _alloc_lastaddr
    _alloctable.clear()
    _alloc_lastaddr = 0


def AllocateSpace(obj, size):
    global _alloc_lastaddr
    global _alloctable

    if obj in _alloctable:  # Already allocated
        return _alloctable[obj]

    else:  # Newly allocate
        allocaddr = _alloc_lastaddr
        _alloctable[obj] = allocaddr
        _alloc_lastaddr += size
        return rlocint.RlocInt(allocaddr, 4)
