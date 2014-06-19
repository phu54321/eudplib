from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVTable
from .eudfunc import EUDFunc
from .ctrlstru import EUDJumpIfNot

f_dwbreak = None
def _dwordbreak_init():
    global f_dwbreak

    vt = EUDVTable(7)

    word = [None] * 2
    byte = [None] * 4
    number, word[0], word[1], byte[0], byte[1], byte[2], byte[3] = vt.GetVariables()

    dwordbreak_begin = Forward()
    dwordbreak_end = Forward()

    f_dwbreak = EUDFunc(dwordbreak_begin, dwordbreak_end, vt, 1, 6)


    # Clear byte[], word[]
    dwordbreak_begin << Trigger(
        actions = [
            [ byte[i].SetNumber(0) for i in range(4) ],
            [ word[i].SetNumber(0) for i in range(2) ]
        ]
    )


    # Chaining
    chain = [Forward() for _ in range(32)]

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16
        byteexp = i % 8
        wordexp = i % 16

        """ Following is equivilant to:
        if number >= 2**i:
            byte[byteidx] += 2**byteexp
            word[wordidx] += 2**wordexp
            number -= 2**i
        """

        chain[i] << NextTrigger()
        nextchain = chain[i - 1] if i > 0 else dwordbreak_end

        EUDJumpIfNot( [number.AtLeast(2**i)], nextchain )

        Trigger(
            nextptr = nextchain,
            actions = [
                byte[byteidx].AddNumber( 2**byteexp ),
                word[wordidx].AddNumber( 2**wordexp ),
                number.SubtractNumber( 2**i )
            ]
        )


    dwordbreak_end << Trigger()

_dwordbreak_init()
