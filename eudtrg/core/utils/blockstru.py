_blockstru = []
_lastblockdict = {}


def CreateBlock(name, userdata):
    block = (name, userdata)
    _blockstru.append(block)

    if name not in _lastblockdict:
        _lastblockdict[name] = []
    _lastblockdict[name].append(block)


def GetLastBlock(name):
    return _lastblockdict[name][-1]


def PopBlock(name):
    lastblock = _blockstru.pop()
    assert lastblock[0] == name, 'Block starting/ending mismatch'
    _lastblockdict[name].pop()
    return lastblock
