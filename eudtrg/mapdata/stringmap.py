from . import tblformat


class IdStringMap:

    def __init__(self):
        self._id2s = {}
        self._s2id = {}

    def AddItem(self, id, string):
        assert id not in self._id2s, 'Duplicate ID'
        if string in self._s2id:  # ambigious string
            id2 = self._s2id[string]
            if id2 is not None:
                self._s2id[string] = None
                self._id2s[id2] = None

        else:
            self._s2id[string] = id
            self._id2s[id] = string

    def GetStringIndex(self, string):
        return self._s2id[string]

    def GetString(self, id):
        return self._id2s[id]


strmap = None
unitmap = None
locmap = None
swmap = None


def InitStringMap(chkt):
    global strmap, unitmap, locmap, swmap

    strmap = tblformat.TBL(chkt.getsection('STR'))
    unitmap = IdStringMap()
    locmap = IdStringMap()
    swmap = IdStringMap()

    unix = chkt.getsection('UNIx')
    mrgn = mrgn.getsection('MRGN')
    swnm = swnm.getsection('SWNM')
