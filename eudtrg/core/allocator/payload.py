#!/usr/bin/python
#-*- coding: utf-8 -*-

from . import rlocint, pbuffer
from . import scaddr


_found_objects = None
_found_objects_set = None
_untraversed_objects = None
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
    global _found_objects
    global _found_objects_set
    global _untraversed_objects

    phase = PHASE_COLLECTING

    objc = ObjCollector()
    _found_objects = []
    _found_objects_set = set()
    _untraversed_objects = []

    # _untraversed_objects.append(root) won't work here, since root can also be
    # Forward() object pointing to Trigger(). Forward().WritePayload() is not
    # defined.
    # Instead, we evaluate root to register objects associated with root to
    # register naturally with GetObjectAddr()
    scaddr.Evaluate(root)

    while _untraversed_objects:
        obj = _untraversed_objects.pop()
        obj.WritePayload(objc)

    _found_objects_set = None
    phase = None


def ConstructPayload(root):
    global phase
    global _found_objects
    global _alloctable

    phase = PHASE_WRITING
    pbuf = pbuffer.PayloadBuffer()

    _alloctable = {}
    lastoffset = 0

    for obj in _found_objects:
        objsize = obj.GetDataSize()
        objaddr = lastoffset
        lastoffset += (objsize + 3) & ~3
        _alloctable[obj] = [objaddr, objsize]

    for obj in _found_objects:
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
    global _found_objects
    global _found_objects_set
    global _untraversed_objects

    if phase == PHASE_COLLECTING:
        if obj not in _found_objects_set:
            _untraversed_objects.append(obj)
            _found_objects.append(obj)
            _found_objects_set.add(obj)

        return rlocint.RlocInt(0, 4)

    elif phase == PHASE_WRITING:
        return rlocint.RlocInt(_alloctable[obj][0], 4)
