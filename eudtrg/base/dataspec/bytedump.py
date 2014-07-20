'''
Defines Db class for uploading arbitary bytes data on SC memory.
'''

from eudtrg import LICENSE #@UnusedImport
from .eudobj import EUDObject

class Db(EUDObject):
    '''
    Db object inserts binary data into starcraft memory. Db object evaluates to
    address where bytes are stored.
    '''
    def __init__(self, content):
        '''
        :param bytes content: Content to put in.
        '''
        super(Db, self).__init__()

        # convert & store
        content = bytes(content)
        self._content = content


    def GetDataSize(self):
        return len(self._content)

    def GetDependencyList(self):
        return []

    def WritePayload(self, buf):
        buf.EmitBytes(self._content)


