from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf


def f_mul(a, b):
    if isinstance(a, vf.EUDVariable) and isinstance(b, vf.EUDVariable):
        return _f_mul(a, b)

    elif isinstance(a, vf.EUDVariable):
        return f_constmul(b)(a)

    elif isinstance(b, vf.EUDVariable):
        return f_constmul(a)(b)

    else:
        return a * b


def f_div(a, b):
    """ returns (a//b, a%b) """
    if isinstance(b, vf.EUDVariable):
        return _f_mul(a, b)

    elif isinstance(a, vf.EUDVariable):
        return f_constdiv(b)(a)

    else:
        return a // b, a % b


# -------


def f_constmul(number):
    if not hasattr(f_constmul, 'mulfdict'):
        f_constmul.mulfdict = {}

    mulfdict = f_constmul.mulfdict

    try:
        return mulfdict[number]
    except KeyError:
        @vf.EUDFunc
        def mulf(a):
            ret = vf.EUDVariable()
            ret << 0
            for i in range(31, -1, -1):
                c.Trigger(
                    conditions=a.AtLeast(2 ** i),
                    actions=[
                        a.SubtractNumber(2 ** i),
                        ret.AddNumber(2 ** i * number)
                    ]
                )
            return ret

        mulfdict[number] = mulf
        return mulf


def f_constdiv(number):
    if not hasattr(f_constdiv, 'divfdict'):
        f_constdiv.divfdict = {}

    divfdict = f_constdiv.divfdict

    try:
        return divfdict[number]
    except KeyError:
        @vf.EUDFunc
        def divf(a):
            ret = vf.EUDVariable()
            ret << 0
            for i in range(31, -1, -1):
                # number too big
                if 2 ** i * number >= 2 ** 32:
                    continue

                c.Trigger(
                    conditions=a.AtLeast(2 ** i * number),
                    actions=[
                        a.SubtractNumber(2 ** i * number),
                        ret.AddNumber(2 ** i)
                    ]
                )
            return ret, a

        divfdict[number] = divf
        return divf

# -------


@vf.EUDFunc
def _f_mul(a, b):
    ret, y0 = vf.EUDCreateVariables(2)

    # Init
    vf.SeqCompute([
        (ret, c.SetTo, 0),
        (y0, c.SetTo, b)
    ])

    chain = [c.Forward() for _ in range(32)]
    chain_y0 = [c.Forward() for _ in range(32)]

    # Calculate chain_y0
    for i in range(32):
        vf.SeqCompute((
            (c.EPD(chain_y0[i]), c.SetTo, y0),
            (y0, c.Add, y0)
        ))
        if i <= 30:
            cs.EUDJumpIf(a.AtMost(2 ** (i + 1) - 1), chain[i])

    # Run multiplication chain
    for i in range(31, -1, -1):
        cy0 = c.Forward()

        chain[i] << c.Trigger(
            conditions=[
                a.AtLeast(2 ** i)
            ],
            actions=[
                a.SubtractNumber(2 ** i),
                cy0 << ret.AddNumber(0)
            ]
        )

        chain_y0[i] << cy0 + 20

    return ret


@vf.EUDFunc
def _f_div(a, b):
    ret, x = vf.EUDCreateVariables(2)

    # Init
    vf.SeqCompute([
        (ret, c.SetTo, 0),
        (x, c.SetTo, b),
    ])

    # Chain c.forward decl
    chain_x0 = [c.Forward() for _ in range(32)]
    chain_x1 = [c.Forward() for _ in range(32)]
    chain = [c.Forward() for _ in range(32)]

    # Fill in chain
    for i in range(32):
        vf.SeqCompute([
            (c.EPD(chain_x0[i]), c.SetTo, x),
            (c.EPD(chain_x1[i]), c.SetTo, x),
        ])

        cs.EUDJumpIf(x.AtLeast(0x8000000), chain[i])

        vf.SeqCompute([
            (x, c.Add, x),
        ])

    # Run division chain
    for i in range(31, -1, -1):
        cx0, cx1 = c.Forward(), c.Forward()
        chain[i] << c.Trigger(
            conditions=[
                cx0 << a.AtLeast(0)
            ],
            actions=[
                cx1 << a.SubtractNumber(0),
                ret.AddNumber(2 ** i)
            ]
        )

        chain_x0[i] << cx0 + 8
        chain_x1[i] << cx1 + 20

    return ret, a  # a : remainder
