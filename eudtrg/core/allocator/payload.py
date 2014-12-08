#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import rlocint, pbuffer
from . import scaddr

_found_objects = []
_found_objects_set = set()
_untraversed_objects = []
_alloctable = {}
_payload_size = 0

PHASE_COLLECTING = 1
PHASE_ALLOCATING = 2
PHASE_WRITING = 3
phase = None

_payload_compress = False

# -------


def CompressPayload(mode):
    global _payload_compress
    if mode not in [True, False]:
        raise TypeError('Invalid type')

    if mode:
        _payload_compress = True
    else:
        _payload_compress = False


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
        if number is not None:
            scaddr.Evaluate(number)

    def WritePack(self, structformat, *arglist):
        for arg in arglist:
            if arg is not None:
                scaddr.Evaluate(arg)

    def WriteBytes(self, b):
        pass

    def WriteSpace(self, spacesize):
        pass


def CollectObjects(root):
    global phase
    global _found_objects
    global _found_objects_set
    global _untraversed_objects
    global _dwoccupmap_dict

    phase = PHASE_COLLECTING

    objc = ObjCollector()
    _found_objects = []
    _found_objects_set = set()
    _dwoccupmap_dict = {}
    _untraversed_objects = []

    # Evaluate root to register root object.
    # root may not have WritePayload() method e.g: Forward()
    scaddr.Evaluate(root)

    while _untraversed_objects:
        obj = _untraversed_objects.pop()
        objc.StartWrite()
        obj.WritePayload(objc)
        _dwoccupmap_dict[obj] = objc.EndWrite()

    _found_objects_set = None
    phase = None


# -------


class ObjAllocator:
    '''
    Object having PayloadBuffer-like interfaces. Collects all objects by
    calling RegisterObject() for every related objects.
    '''

    def __init__(self):
        pass

    def StartWrite(self):
        self._occupmap = []

    def EndWrite(self):
        dlen = (len(self._occupmap) + 3) & ~3
        self._occupmap.extend([0] * (dlen - len(self._occupmap)))

        # Count by dword
        dwoccupmap = []
        for i in range(0, len(self._occupmap), 4):
            dwoccupmap.append(self._occupmap[i:i+4] != [0, 0, 0, 0])

        return dwoccupmap

    def WriteByte(self, number):
        if number is None:
            self._occupmap.append(0)
        else:
            scaddr.Evaluate(number)
            self._occupmap.append(1)

    def WriteWord(self, number):
        if number is None:
            self._occupmap.append((0, 0))
        else:
            scaddr.Evaluate(number)
            self._occupmap.extend((1, 1))

    def WriteDword(self, number):
        if number is None:
            self._occupmap.append((0, 0, 0, 0))
        else:
            scaddr.Evaluate(number)
            self._occupmap.extend((1, 1, 1, 1))

    def WritePack(self, structformat, *arglist):
        ocm = []
        sizedict = {'B': 1, 'H': 2, 'I': 4}
        for i, arg in enumerate(arglist):
            isize = sizedict[structformat[i]]

            if arg is None:
                ocm += [0] * isize
            else:
                scaddr.Evaluate(arg)
                ocm += [1] * isize
        self._occupmap.extend(ocm)

    def WriteBytes(self, b):
        self._occupmap.extend([1] * len(b))

    def WriteSpace(self, spacesize):
        self._occupmap.extend([0] * spacesize)


def AllocObjects():
    global phase
    global _alloctable
    global _payload_size

    phase = PHASE_ALLOCATING

    # Quick and less space-efficient approach
    if not _payload_compress:
        last_alloc_addr = 0
        for obj in _found_objects:
            objsize = (obj.GetDataSize() + 3) & ~3
            _alloctable[obj] = last_alloc_addr, objsize
            last_alloc_addr += objsize
        _payload_size = last_alloc_addr
        phase = None
        return

    obja = ObjAllocator()

    _alloctable = {}
    dwoccupmap_dict = {}
    dwoccupmap_max_size = 0

    # Get occupation map for all objects
    for obj in _found_objects:
        obja.StartWrite()
        obj.WritePayload(obja)
        dwoccupmap = obja.EndWrite()

        dwoccupmap_max_size += len(dwoccupmap)
        dwoccupmap_dict[obj] = dwoccupmap

        # preprocess dwoccupmap
        for i in range(len(dwoccupmap)):
            if dwoccupmap[i] == 0:
                dwoccupmap[i] = -1
            elif i == 0 or dwoccupmap[i - 1] == -1:
                dwoccupmap[i] = i
            else:
                dwoccupmap[i] = dwoccupmap[i - 1]

    # Buffer to sum all dwoccupmaps
    dwoccupmap_sum = [-1] * (dwoccupmap_max_size + 1)

    last_alloc_addr = 0
    for obj in _found_objects:
        dwoccupmap = dwoccupmap_dict[obj]

        # Find appropriate position to allocate object
        j = 0
        while j < len(dwoccupmap):
            if dwoccupmap[j] != -1 and dwoccupmap_sum[last_alloc_addr + j] != -1:  # conflict
                # last_alloc_addr = (dwoccupmap_sum[last_alloc_addr + j] - j) + (j - dwoccupmap[j])
                last_alloc_addr = dwoccupmap_sum[last_alloc_addr + j] - dwoccupmap[j]
                j = 0

            else:
                j += 1

        # Apply occupation map
        for j in range(len(dwoccupmap) - 1, -1, -1):
            curoff = last_alloc_addr + j
            if dwoccupmap[j] != -1 or dwoccupmap_sum[curoff] != -1:
                if dwoccupmap_sum[curoff + 1] == -1:
                    dwoccupmap_sum[curoff] = curoff + 1
                else:
                    dwoccupmap_sum[curoff] = dwoccupmap_sum[curoff + 1]

        objsize = obj.GetDataSize()
        _alloctable[obj] = (last_alloc_addr * 4, objsize)
        if last_alloc_addr * 4 + objsize > _payload_size:
            _payload_size = last_alloc_addr * 4 + objsize


    phase = None


# -------


def ConstructPayload():
    global phase

    phase = PHASE_WRITING

    pbuf = pbuffer.PayloadBuffer(_payload_size)

    for obj in _found_objects:
        objaddr, objsize = _alloctable[obj]

        pbuf.StartWrite(objaddr)
        obj.WritePayload(pbuf)
        written_bytes = pbuf.EndWrite()
        assert written_bytes == objsize, (
            'obj.GetDataSize()(%d) != Real payload size(%d) for object %s'
            % (objsize, written_bytes, obj))

    phase = None
    return pbuf.CreatePayload()


def CreatePayload(root):
    CollectObjects(root)
    AllocObjects()
    print('%d objects found' % len(_found_objects))
    return ConstructPayload()


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

    elif phase == PHASE_ALLOCATING:
        return rlocint.RlocInt(0, 4)

    elif phase == PHASE_WRITING:
        return rlocint.RlocInt(_alloctable[obj][0], 4)
