'''
Defines EUDObject, which means everything uploadable into SC memory.
'''

from eudtrg import LICENSE #@UnusedImport

from ..payload.rlocint import RelocatableInt
from .expr import Expr

class EUDObject(Expr):
    '''
    EUDObject is a base class for uploadable objects. Uploadable objects means that
    object can be uploaded into Starcraft memory. Every resource data and triggers
    should be uploaded to SC memory to have effects. Derived class should implement
    three virtual methods:
     - GetDependencyList : Get list of objects/expressions object depends on.
     - GetDataSize : Get size of object. e.g. Trigger object's size is 2408.
     - WritePayload : Write payload data into given buffer.
    '''
    def __init__(self):
        super().__init__()
        self._address = None

    def SetAddress(self, address):
        '''
        Set address of object. Don't override.
        '''
        assert self._address is None
        self._address = address


    def ResetAddress(self):
        '''
        Returns address of object. Reset address for future usage.
        '''
        assert self._address is not None
        self._address = None


    def EvalImpl(self):
        '''
        Returns address of object. You can override this function for some effects. See
        auxlib/EUDGrp for override example.
        '''
        assert self._address is not None
        return RelocatableInt(self._address, 4)


    def GetDependencyList(self):
        '''
        Get list of objects/expressions object depends on.
        eudtrg automatically traverses through objects, so derived object don't have to
        traverse through other objects. Instead, GetDependencyList should give a
        complete list of objects which derived object directly depends on.
        '''
        raise NotImplementedError("Subclass %s should implement GetDependencyList" % str(type(self)))


    def GetDataSize(self):
        '''
        Get size of object when it is uploaded. e.g. Trigger object's size is 2408.
        '''
        raise NotImplementedError("Subclass %s should implement GetDataSize" % str(type(self)))


    def WritePayload(self, emitbuffer):
        '''
        Write payload data into given buffer.
        WritePayload can write data into emitbuffer using following functions
         - EmitByte  : Emit byte. Byte should be constant
         - EmitWord  : Emit words. Word should be constant
         - EmitDword : Emit dword. Dword can be either constant or object address/epdp.
         - EmitBytes : Emit bytes object.
        eudtrg will raise RuntimeError if object have written payload of size different
        from GetDatasize.
        '''
        raise NotImplementedError("Subclass %s should implement WritePayload" % str(type(self)))

