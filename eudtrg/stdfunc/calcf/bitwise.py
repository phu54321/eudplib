#!/usr/bin/python
# -*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf


def bw_gen(cond):
    @vf.EUDFunc
    def f_bitsize_template(a, b):
        tmp = vf.EUDLightVariable()
        ret = vf.EUDVariable()

        ret << 0

        for i in range(31, -1, -1):
            c.Trigger(
                conditions=[
                    a.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    a.SubtractNumber(2 ** i)
                ]
            )

            c.Trigger(
                conditions=[
                    b.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    b.SubtractNumber(2 ** i)
                ]
            )

            c.Trigger(
                conditions=cond(tmp),
                actions=ret.AddNumber(2 ** i)
            )

            cs.DoActions(tmp.SetNumber(0))

        return ret

    return f_bitsize_template


f_bitand = bw_gen(lambda x: x.Exactly(2))
f_bitor = bw_gen(lambda x: x.AtLeast(1))
f_bitxor = bw_gen(lambda x: x.Exactly(1))

f_bitnand = bw_gen(lambda x: x.Exactly(0))
f_bitnor = bw_gen(lambda x: x.AtMost(1))


@vf.EUDFunc
def f_bitnxor(a, b):
    return f_bitnot(f_bitxor(a, b))


def f_bitnot(a):
    return 0xFFFFFFFF - a
