from eudtrg import LICENSE #@UnusedImport

from ..utils import binio, ubconv

class TBL:
    def __init__(self, content = None):
        #
        # datatb : table of strings                         : string data table
        # dataindextb : string id -> data id                : string offset table
        # stringmap : string -> representative string id
        #
        
        self._datatb = []
        self._stringmap = {}
        self._dataindextb = [] # String starts from #1
        self._capacity = 2 # Size of STR section

        if content is not None:
            self.LoadData(content)
        
            
    def LoadTBL(self, content):
        self._datatb.clear()
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
        
        stringindex = len(self._dataindextb)
        
        # If duplicate text exist -> just proxy it    
        try:
            repr_stringid = self._stringmap[string]
            dataindex = self._dataindextb[repr_stringid]
            self._dataindextb.append(dataindex)
            self._capacity += 2 # just string offset
            
        # Else -> Create new entry
        except KeyError:
            dataindex = len(self._datatb)
            self._stringmap[string] = stringindex
            self._datatb.append(string)
            self._dataindextb.append(dataindex)
            self._capacity += len(string) + 1 + 2 # string + b'\0' + string offset

        assert self._capacity < 65536, 'String table overflow'
        
        return stringindex


    def GetString(self, index):
        if index == 0: return None
        else:
            try:
                return self._datatb[index - 1]
            except IndexError:
                return None


    def GetStringIndex(self, string):
        try:
            return self._stringmap[string] + 1
        
        except KeyError:
            return self.AddString(string) + 1
        

    def SaveTBL(self):
        #
        # datatb : table of strings                         : string data table
        # dataindextb : string id -> data id                : string offset table
        # stringmap : string -> representative string id
        #
        
        outbytes = []

        # calculate offset of each string
        stroffset = []
        outindex = 2 * len(self._dataindextb) + 2
        for s in self._datatb:
            stroffset.append(outindex)
            outindex += len(s) + 1

        # String count
        outbytes.append(binio.i2b2(len(self._dataindextb)))

        # String offsets
        for dataidx in self._dataindextb:
            outbytes.append(binio.i2b2(stroffset[dataidx]))

        # String data
        for s in self._datatb:
            outbytes.append(s)
            outbytes.append(b'\0')

        return b''.join(outbytes)
