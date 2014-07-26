from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from eudtrg.lib.baselib import * #@UnusedWildImport

@EUDFunc
def f_dwbreak(number):
    '''
    Break dword into words & dwords.

    :param number: Number to break.
    :returns: w[0], w[1], b[0], b[1], b[2], b[3] ::
    
        union {
            DWORD number;
            WORD w[2];
            BYTE b[4];
        }
    '''
    word = [None] * 2
    byte = [None] * 4
    word[0], word[1], byte[0], byte[1], byte[2], byte[3] = EUDCreateVariables(6)


    # Clear byte[], word[]
    Trigger(
        actions = [
            [ byte[i].SetNumber(0) for i in range(4) ],
            [ word[i].SetNumber(0) for i in range(2) ]
        ]
    )


    # Chaining
    chain = [Forward() for _ in range(32)]

    dwordbreak_end = Forward()

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


    dwordbreak_end << NextTrigger()
    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]
