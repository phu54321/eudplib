from .. import core as c
from .eudv import EUDVariable


def _VProc(v, actions):
    nexttrg = c.Forward()

    c.Trigger(
        nextptr=v.GetVTable(),
        actions=[actions] + [c.SetNextPtr(v.GetVTable(), nexttrg)]
    )

    nexttrg << c.NextTrigger()


#######################################
# TODO : Optimize this function
#######################################

def SeqCompute(assignpairs):  # Same as _Basic_SeqCompute now.
    for dst, mdt, src in assignpairs:
        try:
            dstepd = c.EPD(dst.GetVariableMemoryAddr())
        except AttributeError:
            dstepd = dst

        if isinstance(src, EUDVariable):
            if mdt == c.SetTo:
                _VProc(src, [
                    src.QueueAssignTo(dstepd)
                ])

            elif mdt == c.Add:
                _VProc(src, [
                    src.QueueAddTo(dstepd)
                ])

            elif mdt == c.Subtract:
                _VProc(src, [
                    src.QueueSubtractTo(dstepd)
                ])

        else:
            c.Trigger(actions=c.SetDeaths(dstepd, mdt, src, 0))
