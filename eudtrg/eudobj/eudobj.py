from ..allocator import scalloc


class EUDObject:

    def __init__(self):
        pass

    def GetDataSize(self):
        raise NotImplementedError('Override')

    def WritePayload(self, pbuffer):
        raise NotImplementedError('Override')
