'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''

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
