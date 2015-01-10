from .. import core as c
from .tpatcher import PatchCondition, PatchAction


def Trigger(conditions=None, actions=None, preserved=True):
    if conditions is None:
        conditions = []
    if actions is None:
        actions = None

    conditions = c.FlattenList(conditions)
    actions = c.FlattenList(actions)

    # Normal
    if len(conditions) <= 16 and len(actions) <= 64:
        for cond in conditions:
            PatchCondition(cond)

        for act in actions:
            PatchAction(act)

        c.RawTrigger(conditions=conditions, actions=actions, preserved=preserved)

    else:
        # Extended trigger
        condts = []
        cend = c.Forward()

        # Check conditions
        for i in range(0, len(conditions), 16):
            conds = conditions[i:i + 16]
            cts = c.Forward()

            for cond in conds:
                PatchCondition(cond)

            nextcond = c.Forward()
            cts << c.RawTrigger(
                nextptr=cend,
                conditions=conds,
                actions=c.SetNextPtr(cts, nextcond)
            )
            nextcond << c.NextTrigger()

            condts.append(cts)

        skipt = c.Forward()
        if not preserved:
            a = c.RawTrigger()
            c.RawTrigger(actions=c.SetNextPtr(a, skipt))

        # Execute actions
        for i in range(0, len(actions), 64):
            acts = actions[i:i + 64]
            for act in acts:
                PatchAction(act)

            c.RawTrigger(actions=acts)

        if not preserved:
            skipt << c.NextTrigger()

        # Revert conditions
        cend << c.NextTrigger()
        for i in range(0, len(condts), 64):
            c.RawTrigger(actions=[c.SetNextPtr(cts, cend) for cts in condts[i:i + 64]])

