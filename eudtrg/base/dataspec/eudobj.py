'''
Defines EUDObject, which means everything uploadable into SC memory.
'''

from eudtrg import LICENSE #@UnusedImport

from ..payload.rlocint import RelocatableInt
from .expr import Expr

class EUDObject(Expr):
    '''
    Base class for objects to be inserted into map.
    '''
    def __init__(self):
        super().__init__()
        self._address = None


    def SetAddress(self, address):
        '''Set address of object ingame. This function is called by eudtrg.
        After this function is called, object shouldn't be modified until
        :meth:'`ResetAddress` is called.

        :param address: Address where the object will be located at ingame.
        '''
        assert self._address is None, 'Might be eudtrg bug. Report this.'
        self._address = address


    def ResetAddress(self):
        '''This function is called by eudtrg. After this function is called, 
        objects can be modified again.
        '''
        assert self._address is not None, 'Might be eudtrg bug. Report this.'
        self._address = None


    def EvalImpl(self):
        '''
        Evaluate object's value. This function returns the object's address by
        default, but you may override the behavior. Return values are cached,
        so EvalImpl will be called at most once for a SaveMap call.

        :returns: Value of object as expression. Default: Address of object.
        '''
        assert self._address is not None, 'GetDependencyList of some classes are incomplete.'
        return RelocatableInt(self._address, 4)


    def GetMPQDependencyList(self):
        '''
        Get list of files this object needs to be inside MPQ.

        :returns: List of (MPQ file path, bytes). Default: [] If different
        contents share the same MPQ filename, :func:`SaveMap` will raise
        RuntimeError.
        '''
        return []

    def GetDependencyList(self):
        '''
        Get list of objects or expressions the object needs. Objects in this
        list are also inserted to the map when the object is being inserted.

        :returns: Objects the object depends on. Default: []
        '''
        return []


    def GetDataSize(self):
        '''
        :returns: Size of object in SC memory. Default: 0
        '''
        return 0


    def WritePayload(self, emitbuffer):
        '''
        This function should write data into buffer. Size of written data
        should match :meth:`GetDataSize.

        :param emitbuffer: Buffer to write data to.
        :type emitbuffer: :class:`PayloadBuffer`

        :raises RuntimeError: Size of written data is different from what
            :meth:`GetDataSize tells.
        '''
        pass

