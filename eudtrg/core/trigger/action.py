from ..allocator import SCMemAddr, Evaluate, IsValidSCMemAddr


class Action(SCMemAddr):

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
       +1D   internal[3
     ======  ============= ========  ==========
    '''

    def __init__(self, locid1, strid, wavid, time, player1, player2,
                 unitid, acttype, amount, flags):
        '''
        See :mod:`eudtrg.base.stocktrg` for stock actions list.
        '''
        super().__init__(self)

        assert IsValidSCMemAddr(locid1), 'Invalid arg %s' % locid1
        assert IsValidSCMemAddr(strid), 'Invalid arg %s' % strid
        assert IsValidSCMemAddr(wavid), 'Invalid arg %s' % wavid
        assert IsValidSCMemAddr(time), 'Invalid arg %s' % time
        assert IsValidSCMemAddr(player1), 'Invalid arg %s' % player1
        assert IsValidSCMemAddr(player2), 'Invalid arg %s' % player2
        assert IsValidSCMemAddr(unitid), 'Invalid arg %s' % unitid
        assert IsValidSCMemAddr(acttype), 'Invalid arg %s' % acttype
        assert IsValidSCMemAddr(amount), 'Invalid arg %s' % amount
        assert IsValidSCMemAddr(flags), 'Invalid arg %s' % flags

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

    def Disable(self):
        self._flags |= 2

    def SetParentTrigger(self, trg, index):
        assert self._parenttrg is None, (
            'Action cannot be shared by two triggers.'
            'Deep copy each conditions')

        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 64, 'WTF'

        self._parenttrg = trg
        self._actindex = index

    # -------

    def Evaluate(self):
        return Evaluate(self._parenttrg) + 8 + 320 + 32 * self._actindex

    def WritePayload(self, pbuffer):
        pbuffer.WritePack(
            'IIIIIIHBBBBH',
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
            0,
            0
        )
