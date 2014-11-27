from ..eudobj import EUDObject
from ..utils import FlattenList
from .triggerscope import NextTrigger, _RegisterTrigger
from .condition import Condition
from .action import Action


class Trigger(EUDObject):

    def __init__(
        self,
        nextptr=None,
        conditions=None,
        actions=None,
        preserved=True
    ):
        super().__init__()

        _RegisterTrigger(self)  # This should be called before (1)

        if nextptr is None:
            nextptr = NextTrigger()  # (1)

        if conditions is None:
            conditions = []

        if actions is None:
            actions = []

        conditions = FlattenList(conditions)
        actions = FlattenList(actions)

        assert len(conditions) <= 16, 'Too many conditions'
        assert len(actions) <= 64, 'Too many actions'

        self._nextptr = nextptr
        self._conditions = conditions
        self._actions = actions
        self._preserved = preserved

        for i, cond in enumerate(self._conditions):
            assert isinstance(cond, Condition)
            cond.SetParentTrigger(self, i)

        for i, act in enumerate(self._actions):
            assert isinstance(act, Action)
            act.SetParentTrigger(self, i)

    def GetDataSize(self):
        return 2408

    def WritePayload(self, pbuffer):
        pbuffer.WriteDword(0)
        pbuffer.WriteDword(self._nextptr)

        # Conditions
        for cond in self._conditions:
            cond.WritePayload(pbuffer)

        pbuffer.WriteBytes(bytes(20 * (16 - len(self._conditions))))

        # Actions
        for act in self._actions:
            act.WritePayload(pbuffer)

        pbuffer.WriteBytes(bytes(32 * (64 - len(self._actions))))

        # Preserved flag

        if self._preserved:
            pbuffer.WriteDword(4)

        else:
            pbuffer.WriteDword(0)

        pbuffer.WriteBytes(bytes(28))
