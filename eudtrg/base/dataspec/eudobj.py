from eudtrg import LICENSE  # @UnusedImport

from .rlocint import RelocatableInt
from .expr import Expr


class EUDObject(Expr):

    '''
    Base class for uploadable objects. Uploadable objects objects having data
    to be inserted into SC Memory. Every EUDObject corresponds to one memory
    chunk inside SC Memory. EUDObject creates data to put inside memory chunk.

    For example, every trigger in Starcraft is just a 2408byte memory chunk.
    :class:`eudtrg.Trigger` refers to that memory chunk, and can create 2408
    byte data to put inside it.
    '''

    def __init__(self):
        super().__init__()
        self._address = None

    def SetAddress(self, address):
        '''
        Called by eudtrg when address of object is fixed. You won't need to
        override this function.
        '''
        assert self._address is None, 'Might be eudtrg bug. Report this.'
        self._address = address

    def ResetAddress(self):
        '''
        Reset object address. Called after payload is successfully injected.
        '''
        assert self._address is not None, 'Might be eudtrg bug. Report this.'
        self._address = None

    def EvalImpl(self):
        '''
        Overrides :meth:`eudtrg.Expr.EvalImpl` .

        :returns: What this object should evaluate to. Default: Address of
            object.
        '''
        assert self._address is not None, (
            'GetDependencyList of some classes are incomplete.')
        return RelocatableInt(self._address, 4)

    def GetDependencyList(self):
        '''
        Overrides :meth:`eudtrg.Expr.GetDependencyList` .

        :returns: List of Expr instances this object depends on. Default:
            Empty list.
        '''
        return []

    def GetDataSize(self):
        '''
        :returns: Size of data inside SC Memory. Default: 0
        '''
        return 0

    def WritePayload(self, emitbuffer):
        '''
        Writes payload(data) to buffer. Users may use:

        - emitbuffer.EmitByte(b) : Emit 1 byte(b) to buffer. b should be const.
        - emitbuffer.EmitWord(w) : Emit 1 word(w) to buffer. w should be const.
        - emitbuffer.EmitDword(dw) : Emit 1 dword(dw) to buffer. Dword should
          be constant or should be placed in 4byte boundary : bytes multiple of
          4 were emitted before EmitDword() call.

        emitbuffer is always aligned to 4byte boundary when WritePayload is
        called.

       :param emitbuffer: Output buffer. Write payload here.

        '''
        pass
