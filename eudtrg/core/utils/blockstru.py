class BlockStruManager:

    def __init__(self):
        self._blockstru = []
        self._lastblockdict = {}

    def empty(self):
        return not self._blockstru


_current_bsm = None


def SetCurrentBlockStruManager(bsm):
    global _current_bsm
    old_bsm = _current_bsm
    _current_bsm = bsm
    return old_bsm


def CreateBlock(name, userdata):
    _blockstru = _current_bsm._blockstru
    _lastblockdict = _current_bsm._lastblockdict

    block = (name, userdata)
    _blockstru.append(block)

    if name not in _lastblockdict:
        _lastblockdict[name] = []
    _lastblockdict[name].append(block)


def GetLastBlock(name):
    _lastblockdict = _current_bsm._lastblockdict

    return _lastblockdict[name][-1]


def PopBlock(name):
    _blockstru = _current_bsm._blockstru
    _lastblockdict = _current_bsm._lastblockdict

    lastblock = _blockstru.pop()
    assert lastblock[0] == name, 'Block starting/ending mismatch'
    _lastblockdict[name].pop()
    return lastblock
