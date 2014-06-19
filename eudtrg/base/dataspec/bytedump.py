from eudtrg import LICENSE #@UnusedImport
from .eudobj import EUDObject

class Db(EUDObject):
    """
    Initalize db class with binary contents. Constructor accepts anything
    convertible to bytes type.
    """
    def __init__(self, content):
        super(Db, self).__init__()

        # convert & store
        content = bytes(content)
        self._content = content

    def GetDataSize(self):
        return len(self._content)

    def GetDependencyList(self):
        return []

    def WritePayloadChunk(self, buf):
        buf.EmitBytes(self._content)


