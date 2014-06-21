'''
Defines Db class for uploading arbitary bytes data on SC memory.
'''

from eudtrg import LICENSE #@UnusedImport
from .eudobj import EUDObject

class Db(EUDObject):
    '''
    Object for uploading arbitary bytestream into starcraft memory. You can store
    bytes objects and reference to this object when you need its content. Useful
    for uploading custom resources into SC memory. One of the simplest EUDObjects.
    '''
    def __init__(self, content):
        '''
        content : Bytes/Bytes-convertible object which Db class should contain.
        '''
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


