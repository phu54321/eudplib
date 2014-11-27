from ..allocator import SCMemAddr
from ..allocator.payload import GetObjectAddr


class EUDObject(SCMemAddr):

    '''Class for standalone object
    '''

    def __init__(self):
        super().__init__(self)

    def Evaluate(self):
        return GetObjectAddr(self)

    def GetDataSize(self):
        raise NotImplementedError('Override')

    def WritePayload(self, pbuffer):
        raise NotImplementedError('Override')
