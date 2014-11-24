from . import scalloc


class EUDObject:

    def __init__(self):
        pass

    def GetMemoryAddr(self):
        return scalloc.AllocateSpace(self)

    def GetDataSize(self):
        raise NotImplementedError('Override')

    def WritePayload(self, payload):
        raise NotImplementedError('Override')
