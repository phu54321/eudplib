'''
Defines EUDObject, which means everything uploadable into SC memory.
'''

from eudtrg import LICENSE #@UnusedImport

from ..payload.rlocint import RelocatableInt
from .expr import Expr

class EUDObject(Expr):
    '''
    EUDObject is a base class for uploadable objects, which can be placed in
    starcraft memory after map loads. Derived class should implement three
    virtual methods:
     - GetDependencyList : Get list of objects/expressions object depends on.
     - GetDataSize : Get size of object. e.g. Trigger object's size is 2408.
     - WritePayload : Write payload data into given buffer.
    '''
    def __init__(self):
        super().__init__()
        self._address = None


    def SetAddress(self, address):
        '''
        Set address of object. After this function is called, you can cache
        values of EvalImpl, GetDependencyList, GetDataSize, WritePayload.
        '''
        assert self._address is None
        self._address = address


    def ResetAddress(self):
        '''
        Returns address of object. Reset address for future usage. You should
        invalidate caches regarding EvalImpl, GetDependencyList, GetDataSize,
        WritePayload after this function is called.
        '''
        assert self._address is not None
        self._address = None


    def EvalImpl(self):
        '''
        Returns nummerical value of this object. This function returns address
        of the object by default, but you may override this behavior.
        '''
        assert self._address is not None
        return RelocatableInt(self._address, 4)


    def GetDependencyList(self):
        '''
        Get list of objects/expressions object depends on.
        eudtrg automatically traverses through objects, so object do not have
        to, and should not traverse through other objects. GetDependencyList
        should give complete list of objects which object directly depends on.
        '''
        raise NotImplementedError("Subclass %s should implement GetDependencyList" % str(type(self)))


    def GetDataSize(self):
        '''
        Get size of object when it is uploaded into Starcraft memory.
        '''
        raise NotImplementedError("Subclass %s should implement GetDataSize" % str(type(self)))


    def WritePayload(self, emitbuffer):
        '''
        Write payload data into given buffer.
        WritePayload can write data into emitbuffer using following functions
         - EmitByte  : Emit byte. Byte should be constant
         - EmitWord  : Emit words. Word should be constant
         - EmitDword : Emit dword. Dword can be either constant or expression.
         - EmitBytes : Emit bytes object.
        eudtrg will raise RuntimeError if object writes more or less bytes than
        specified by GetDataSize.
        '''
        raise NotImplementedError("Subclass %s should implement WritePayload" % str(type(self)))

