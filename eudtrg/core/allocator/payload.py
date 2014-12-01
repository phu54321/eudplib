from . import rlocint, pbuffer
from . import scaddr


_searched_objects = None
_searched_objects_set = None
_unsearched_objects = None
_alloctable = None


class ObjCollector:

    '''
    Object having PayloadBuffer-like interfaces. Collects all objects by
    calling RegisterObject() for every related objects.
    '''

    def __init__(self):
        pass

    def StartWrite(self):
        pass

    def EndWrite(self):
        pass

    def WriteByte(self, number):
        pass

    def WriteWord(self, number):
        pass

    def WriteDword(self, number):
        scaddr.Evaluate(number)

    def WritePack(self, structformat, *arglist):
        for arg in arglist:
            scaddr.Evaluate(arg)

    def WriteBytes(self, b):
        pass


PHASE_COLLECTING = 1
PHASE_WRITING = 2
phase = None


def CollectObjects(root):
    global phase
    global _searched_objects, _searched_objects_set
    global _unsearched_objects

    phase = PHASE_COLLECTING

    objc = ObjCollector()
    _searched_objects = []
    _searched_objects_set = set()
    _unsearched_objects = []

    # _unsearched_objects.append(root) won't work here, since root can also be
    # Forward() object pointing to Trigger(). Forward().WritePayload() is not
    # defined.
    # Instead, we evaluate root to register objects associated with root to
    # register naturally with GetObjectAddr()
    scaddr.Evaluate(root)

    while _unsearched_objects:
        obj = _unsearched_objects.pop()
        _searched_objects.append(obj)
        _searched_objects_set.add(obj)
        obj.WritePayload(objc)

    _searched_objects_set = None
    phase = None


def ConstructPayload(root):
    global phase
    global _searched_objects
    global _alloctable

    phase = PHASE_WRITING
    pbuf = pbuffer.PayloadBuffer()

    _alloctable = {}
    lastoffset = 0

    for obj in _searched_objects:
        objsize = obj.GetDataSize()
        objaddr = lastoffset
        lastoffset += (objsize + 3) & ~3
        _alloctable[obj] = [objaddr, objsize]
        print('Registering object %s at 0x%08X' % (obj, objaddr))

    for obj in _searched_objects:
        objsize = _alloctable[obj][1]

        pbuf.StartWrite()
        obj.WritePayload(pbuf)
        written_byten = pbuf.EndWrite()
        assert written_byten == objsize, (
            'obj.GetDataSize()(%d) != Real payload size(%d)'
            % (objsize, written_byten))

    phase = None
    return pbuf.CreatePayload()


def CreatePayload(root):
    CollectObjects(root)
    return ConstructPayload(root)


def GetObjectAddr(obj):
    global _alloctable
    global _searched_objects
    global _unsearched_objects

    if phase == PHASE_COLLECTING:
        if obj not in _searched_objects:
            _unsearched_objects.append(obj)

        return rlocint.RlocInt(0, 4)

    elif phase == PHASE_WRITING:
        return rlocint.RlocInt(_alloctable[obj][0], 4)
