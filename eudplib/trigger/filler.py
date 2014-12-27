'''
Defines subfunctions used inside variable-mixed trigger
'''

from .. import core as c

def filldw(dstepd, v1):
    c.SeqCompute((
        (dstepd, c.SetTo, v1),
    ))

@c.EUDFunc
def fillwbb(dstepd, v1, v2, v3):
    ret = c.EUDVariable()
    ret << 0

    for i in range(15, -1, -1):
        c.BasicTrigger(
            conditions=v1.AtLeast(2**i),
            actions=[
                v1.SubtractNumber(2**i),
                ret.AddNumber(2**i)
            ]
        )

    for i in range(7, -1, -1):
        c.BasicTrigger(
            conditions=v2.AtLeast(2**i),
            actions=[
                v2.SubtractNumber(2**i),
                ret.AddNumber(2**(i+16))
            ]
        )

    for i in range(7, -1, -1):
        c.BasicTrigger(
            conditions=v3.AtLeast(2**i),
            actions=[
                v3.SubtractNumber(2**i),
                ret.AddNumber(2**(i+24))
            ]
        )

    return ret


@c.EUDFunc
def fillbbbb(dstepd, v1, v2, v3, v4):
    ret = c.EUDVariable()
    ret << 0

    vlist = (v1, v2, v3, v4)
    for i, v in enumerate(vlist):
        lsf = 8 * i
        for i in range(7, -1, -1):
            c.BasicTrigger(
                conditions=v.AtLeast(2**i),
                actions=[
                    v.SubtractNumber(2**i),
                    ret.AddNumber(2**(i+lsf))
                ]
            )

    return ret
