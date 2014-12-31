from .. import core as c
from .tpatcher import PatchCondition, PatchAction


def Branch(conditions, ontrue, onfalse):
    flag = c.EUDLightVariable()
    flag << 0

    conditions = c.FlattenList(conditions)

    if len(conditions) == 0:
        c.RawTrigger(nextptr=ontrue)  # Just jump
        return

    brtriggers = []
    onfalsetrg = c.Forward()

    # Check all conditions
    for i in range(0, len(conditions), 16):
        conds = conditions[i:i + 16]
        for cond in conds:
            PatchCondition(cond)

        brtrg = c.Forward()
        nxtrg = c.Forward()
        brtrg << c.RawTrigger(
            nextptr=onfalsetrg,
            conditions=conds,
            actions=c.SetNextPtr(brtrg, nxtrg)
        )

        nxtrg << c.NextTrigger()
        brtriggers.append(brtrg)

    # On true : revert all
    revertacts = [c.SetNextPtr(brtrg, onfalsetrg) for brtrg in brtriggers]
    for i in range(0, len(revertacts), 64):
        if i + 64 < len(revertacts):
            c.RawTrigger(actions=revertacts[i:i + 64])
        else:
            c.RawTrigger(nextptr=ontrue, actions=revertacts[i:i + 64])

    # on false
    if len(brtriggers) >= 2:
        onfalsetrg << c.NextTrigger()
        revertacts = [c.SetNextPtr(brtrg, onfalsetrg) for brtrg in brtriggers][:-1]  # Revert all except last brtrg
        for i in range(0, len(revertacts), 64):
            if i + 64 < len(revertacts):
                c.RawTrigger(actions=revertacts[i:i + 64])
            else:
                c.RawTrigger(nextptr=onfalsetrg, actions=revertacts[i:i + 64])
    else:
        onfalsetrg << onfalse

