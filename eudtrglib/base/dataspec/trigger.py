'''
Defines trigger-related items.
'''

from eudtrglib import LICENSE #@UnusedImport

from .eudobj import EUDObject
from .expr import Expr, IsValidExpr, Evaluate
from .rlocint import RelocatableInt
from ..utils.utils import FlattenList




# Used while evaluating Trigger
_next_triggers_stack = []
_next_triggers = []
_last_trigger = [None]
class NextTrigger(Expr):
    '''
    Create reference to next declared trigger.
    '''

    def __init__(self):
        self._trg = triggerend
        _next_triggers.append(self)

    def SetTrigger(self, trg):
        self._trg = trg

    def GetDependencyList(self):
        return [self._trg]

    def EvalImpl(self):
        return Evaluate(self._trg)





def PushTriggerScope():
    '''
    Creates trigger scope. Triggers inside a scope is isolated from outside.
    Triggers from different scope won't have their nextptr linked implicitly.
    You can still link triggers in other scopes by setting nextptr explicitly.
    This function is used in conjunction with :func:`PopTriggerScope()`.

    example ::

        a = Trigger()
        PushTriggerScope() ################
        b = Trigger()          isolated
        c = Trigger()          isolated
        PopTriggerScope()  ################
        d = Trigger()
    
    '''

    global _next_triggers
    _next_triggers_stack.append(_next_triggers)
    _last_trigger.append(None)
    _next_triggers = []


def PopTriggerScope():
    '''
    Exits trigger scope. Used in conjunction with :func:`PushTriggerScope()`.
    '''

    global _next_triggers
    assert not _next_triggers, 'NextTrigger() has no meanings at the end of the scope'
    _last_trigger.pop()
    _next_triggers = _next_triggers_stack.pop()




class Trigger(EUDObject):
    '''
    Object representing trigger. Trigger has following fields
     - nextptr : Pointer to next executed trigger.
     - conditions : Conditions. Trigger executes if every conditions are met.
     - actions : Actions. Actions are executed in sequential order.
    '''

    def __init__(self, nextptr = None, conditions = [], actions = [], preserved = True):
        '''
        Constructor of Trigger class.

        :param nextptr: Trigger to be executed after this trigger. If not
            specified, nextptr of the trigger is automatically set to the next
            created triggers in the same scope. Default: None(Unspecified).
        :param conditions: Nested List of :class:`Condition`.
        :param actions: Nested List of :class:`Action`.
        :param preserved: Trigger is preserved. Default: True
        :type preserved: bool
        '''
        global _last_trigger
        global _next_triggers


        super().__init__()

        conditions = FlattenList(conditions)
        actions = FlattenList(actions)

        # basic assertion
        assert len(conditions) <= 16
        assert len(actions) <= 64

        for cond in conditions:
            assert type(cond) is Condition

        for act in actions:
            assert type(act) is Action


        # Set fields
        if nextptr:
            assert IsValidExpr(nextptr), "nextptr is not an addressable object or expression."

        self._nextptr = nextptr
        self._conditions = conditions
        self._actions = actions
        self._nexttrg = 0xFFFFFFFF
        self._preserved = preserved

        # Set parents of conditions and actions.
        for i, cond in enumerate(conditions):
            cond.SetParentTrigger(self, i)

        for i, act in enumerate(actions):
            act.SetParentTrigger(self, i)



        # link previous trigger with this, if previous trigger had not specified nextptr.
        last_trigger = _last_trigger.pop()
        if last_trigger:
            if last_trigger._nextptr is None:
                last_trigger._nextptr = self

            last_trigger._nexttrg = self

        last_trigger = self
        _last_trigger.append(last_trigger)

        # link NextTriggers
        for nt in _next_triggers:
            nt.SetTrigger(self)

        _next_triggers = []


    # function needed for payloadmanager
    def GetDataSize(self):
        return 2408

    def GetDependencyList(self):
        return [self._nextptr] + self._conditions + self._actions


    def WritePayload(self, buf):
        _next_trigger = self._nexttrg

        buf.EmitDword(0)
        if self._nextptr is None:
            buf.EmitDword(triggerend) # default behavior.
        else:
            buf.EmitDword(self._nextptr)

        for cond in self._conditions:
            cond.WritePayload(buf)

        buf.EmitBytes(bytes(20 * (16 - len(self._conditions))))

        for act in self._actions:
            act.WritePayload(buf)

        buf.EmitBytes(bytes(32 * (64 - len(self._actions))))

        # 04 00 00 00 means 'preserve trigger'.
        if self._preserved:
            buf.EmitBytes(b'\x04\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
        else:
            buf.EmitBytes(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')





class Condition(Expr):
    '''
    Condition class.

    Memory layout:

     ======  =============  ========  ===========
     Offset  Field name     Position  EPD Player   
     ======  =============  ========  ===========
       +00   locid           dword0   EPD(cond)+0  
       +04   player          dword1   EPD(cond)+1  
       +08   amount          dword2   EPD(cond)+2  
       +0C   unitid          dword3   EPD(cond)+3  
       +0E   comparison                            
       +0F   condtype                              
       +10   restype         dword4   EPD(cond)+4  
       +11   flags                                 
       +12   internal[2]                           
     ======  =============  ========  ===========
    '''

    def __init__(self, locid, player, amount, unitid, comparison, condtype, restype, flags):
        '''
        See :mod:`eudtrglib.base.stocktrg` for stock conditions list.
        '''
        assert IsValidExpr(locid)      , 'locid = %s is not a valid expression!' % str(locid)
        assert IsValidExpr(player)     , 'player = %s is not a valid expression!' % str(player)
        assert IsValidExpr(amount)     , 'amount = %s is not a valid expression!' % str(amount)
        assert IsValidExpr(unitid)     , 'unitid = %s is not a valid expression!' % str(unitid)
        assert IsValidExpr(comparison) , 'comparison = %s is not a valid expression!' % str(comparison)
        assert IsValidExpr(condtype)   , 'condtype = %s is not a valid expression!' % str(condtype)
        assert IsValidExpr(restype)    , 'restype = %s is not a valid expression!' % str(restype)
        assert IsValidExpr(flags)      , 'flags = %s is not a valid expression!' % str(flags)

        super(Condition, self).__init__()
        self._locid = locid
        self._player = player
        self._amount = amount
        self._unitid = unitid
        self._comparison = comparison
        self._condtype = condtype
        self._restype = restype
        self._flags = flags

        self._parenttrg = None
        self._condindex = None

    def SetParentTrigger(self, trg, index):
        assert self._parenttrg is None, 'Condition cannot be shared by two triggers. Deep copy each conditions'
        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 16, 'WTF'

        self._parenttrg = trg
        self._condindex = index

    def Disable(self):
        self._flags |= 2



    # Expr
    def Evaluate(self):
        return Evaluate(self._parenttrg) + RelocatableInt(8 + 20 * self._condindex, 0)

    # Used by Trigger::GetDependencyList
    def GetDependencyList(self):
        assert self._parenttrg, 'Condition must be inside a trigger'
        return [
            self._parenttrg,
            self._locid,
            self._player,
            self._amount,
            self._unitid,
            self._comparison,
            self._condtype,
            self._restype,
            self._flags,
        ]

    # Used by Trigger::WritePayload
    def WritePayload(self, buf):
        buf.EmitPack('IIIHBBBBH', self._locid, self._player, self._amount,
            self._unitid, self._comparison, self._condtype, self._restype, self._flags, 0)





class Action(Expr):
    '''
    Action class.

    Memory layout.

     ======  ============= ========  ==========
     Offset  Field Name    Position  EPD Player  
     ======  ============= ========  ==========
       +00   locid1         dword0   EPD(act)+0  
       +04   strid          dword1   EPD(act)+1  
       +08   wavid          dword2   EPD(act)+2  
       +0C   time           dword3   EPD(act)+3  
       +10   player1        dword4   EPD(act)+4  
       +14   player2        dword5   EPD(act)+5  
       +18   unitid         dword6   EPD(act)+6  
       +1A   acttype                             
       +1B   amount                              
       +1C   flags          dword7   EPD(act)+7  
       +1D   internal[3]                         
     ======  ============= ========  ==========
    '''

    def __init__(self, locid1, strid, wavid, time, player1, player2, unitid, acttype, amount, flags):
        '''
        See :mod:`eudtrglib.base.stocktrg` for stock actions list.
        '''
        super(Action, self).__init__()

        assert IsValidExpr(locid1)  , 'locid1 = %s is not a valid expression!' % str(locid1)
        assert IsValidExpr(strid)   , 'strid = %s is not a valid expression!' % str(strid)
        assert IsValidExpr(wavid)   , 'wavid = %s is not a valid expression!' % str(wavid)
        assert IsValidExpr(time)    , 'time = %s is not a valid expression!' % str(time)
        assert IsValidExpr(player1) , 'player1 = %s is not a valid expression!' % str(player1)
        assert IsValidExpr(player2) , 'player2 = %s is not a valid expression!' % str(player2)
        assert IsValidExpr(unitid)  , 'unitid = %s is not a valid expression!' % str(unitid)
        assert IsValidExpr(acttype) , 'acttype = %s is not a valid expression!' % str(acttype)
        assert IsValidExpr(amount)  , 'amount = %s is not a valid expression!' % str(amount)
        assert IsValidExpr(flags)   , 'flags = %s is not a valid expression!' % str(flags)

        self._locid1 = locid1
        self._strid = strid
        self._wavid = wavid
        self._time = time
        self._player1 = player1
        self._player2 = player2
        self._unitid = unitid
        self._acttype = acttype
        self._amount = amount
        self._flags = flags

        self._parenttrg = None
        self._actindex = None

    def SetParentTrigger(self, trg, index):
        assert self._parenttrg is None, 'Action cannot be shared by two triggers. Deep copy each conditions'
        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 64, 'WTF'

        self._parenttrg = trg
        self._actindex = index

    def Disable(self):
        self._flags |= 2



    # Expr
    def Evaluate(self):
        return Evaluate(self._parenttrg) + RelocatableInt(8 + 320 + 32 * self._actindex, 0)

    # Used in Trigger::GetDependencyList
    def GetDependencyList(self):
        assert self._parenttrg, 'Action must be inside a trigger'
        return [
            self._parenttrg,
            self._locid1,
            self._strid,
            self._wavid,
            self._time,
            self._player1,
            self._player2,
            self._unitid,
            self._acttype,
            self._amount,
            self._flags,
        ]


    # Used in Trigger::WritePayload
    def WritePayload(self, buf):
        buf.EmitPack('IIIIIIHBBBBH', self._locid1, self._strid, self._wavid, self._time, self._player1,
            self._player2, self._unitid, self._acttype, self._amount, self._flags, 0, 0)



def Disabled(item):
    '''
    Make condition/action disabled.
    >>> Disabled(SetDeaths(Player1, SetTo, 1234, 'Terran Marine'))

    :param item: Condition/Action to disable
    :returns: Disabled condition/action.
    '''
    item.Disable()
    return item


# predefined constants
#: Indicates 'End of trigger execution'. Executing triggend will terminate
#: Starcraft trigger engine.
class triggerend(Expr):
    def __init__(self):
        pass

    def GetDependencyList():
        return []

    def EvalImpl():
        return 0xFFFFFFFF

# bigger than 0x80000000