from . import rlocint, pbuffer


_alloctable = {}
_alloc_lastaddr = 0
_unwritten_objs = list()


def CreatePayload(root):
    global _alloctable, _alloc_lastaddr
    _alloctable.clear()
    _alloc_lastaddr = 0

    RegisterObject(root)

    pbuf = pbuffer.PayloadBuffer()

    while _unwritten_objs:
        obj = _unwritten_objs.pop()
        pbuf.StartWrite()
        obj.WritePayload(pbuf)
        pbuf.EndWrite()

    return pbuf.CreatePayload()


def RegisterObject(obj):
    global _alloc_lastaddr
    global _alloctable

    if obj not in _alloctable:
        allocaddr = _alloc_lastaddr
        _alloctable[obj] = allocaddr
        _alloc_lastaddr += (obj.GetDataSize() + 3) & -3
        _unwritten_objs.append(obj)


def GetObjectAddr(obj):
    global _alloc_lastaddr
    global _alloctable

    RegisterObject(obj)
    return rlocint.RlocInt(_alloctable[obj], 4)
