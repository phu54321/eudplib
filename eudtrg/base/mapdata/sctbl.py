from eudtrg import LICENSE #@UnusedImport

from ..utils import binio, ubconv

class TBL:
    def __init__(self, content = None):
        self._stringarr = []
        self._stringmap = {}
        self._capacity = 2 # Size of STR section

        if content is not None:
            self.LoadData(content)
        
            
    def LoadTBL(self, content):
        self._stringarr.clear()
        self._stringmap.clear()
        self._capacity = 2
        
        stringcount = binio.b2i2(content, 0)
        for i in range(stringcount):
            i += 1
            stringoffset = binio.b2i2(content, i * 2)
            send = stringoffset
            while content[send] != 0:
                send += 1

            string = content[stringoffset:send]
            self.AddString(string)

    def AddString(self, string):
        if type(string) is str:
            string = ubconv.u2b(string) # Starcraft uses multibyte encoding.

        # Update properties
        self._capacity += len(string) + 1 + 2 # string + b'\0' + string offset
        self._stringarr.append(string)
        stringindex = len(self._stringarr)
        self._stringmap[string] = stringindex

        assert self._capacity < 65536, 'String table overflow'

        # Beware : self._stringarr[stringindex - 1] == string.
        return stringindex

    def GetString(self, index):
        if index == 0: return None
        else:
            try:
                return self._stringarr[index]
            except IndexError:
                return None


    def GetStringIndex(self, string):
        try:
            return self._stringmap[string]
        except KeyError:
            return self.AddString(string)

    def SaveTBL(self):
        datatb = []

        # calculate offset of each string
        stroffset = []
        outindex = 2 * len(self._stringarr) + 2
        for s in self._stringarr:
            stroffset.append(outindex)
            outindex += len(s) + 1

        # Collect data

        # String count
        datatb.append(binio.b2i2(len(self._stringarr)))

        # String offsets
        for off in stroffset:
            datatb.append(binio.b2i2(off))

        # String datas
        for s in self._stringarr:
            datatb.append(s)
            datatb.append(b'\0')

        return b''.join(datatb)
