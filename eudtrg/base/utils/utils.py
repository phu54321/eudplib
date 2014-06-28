'''
Useful utilities. You may freely use these functions.
'''

from eudtrg import LICENSE #@UnusedImport

def EPD(offset):
    '''
    Offset to EPD player.
    '''
    return (offset - 0x0058A364) // 4


'''
Nested list / Single item -> Flat list
 ex) FlattenList([a, [b, c], d]) -> [a, b, c, d]
 ex) FlattenList([a, b, c])      -> [a, b, c]
 ex) FlattenList(a)              -> [a]
'''
def FlattenList(l):
    try:
        ret = []
        for item in l:
            ret.extend(FlattenList(item))
        return ret

    except TypeError: # l is not iterable
        return [l]

def SCM2Text(s):
    #
    # normal -> xdigitinput1 -> xdigitinput2 -> xdigitinput3 -> normal
    #        '<'           xdigit          xdigit            '>'
    #                        -> normal
    #                       '>' emit '<>'
    #                                        -> normal
    #                                        '>' emit x00
    #                                                        -> normal
    #                                                      xdigit/normal  emit '<xx'
    def toxdigit(i):
        if '0' <= i <= '9':
            return ord(i) - 48
        elif 'a' <= i <= 'z':
            return ord(i) - 97 + 10
        elif 'A' <= i <= 'Z':
            return ord(i) - 65 + 10
        else:
            return None

    state = 0
    buf = [None, None]
    bufch = [None, None]
    out = []

    # simple fsm
    for i in s:
        print(i, state)
        if state == 0:
            if i == '<':
                state = 1
            else:
                out.append(i)

        elif state == 1:
            xdi = toxdigit(i)
            if xdi is not None:
                buf[0] = xdi
                bufch[0] = i
                state = 2

            else:
                out.extend(['<', i])
                state = 0

        elif state == 2:
            xdi = toxdigit(i)
            if xdi is not None:
                buf[1] = xdi
                bufch[1] = i
                state = 3

            elif i == '>':
                out.append(chr(buf[0]))
                state = 0

            else:
                out.extend(['<', bufch[0], i])
                state = 0

        elif state == 3:
            if i == '>':
                out.append(chr(buf[0] * 16 + buf[1]))
                state = 0

            else:
                out.extend(['<', bufch[0], bufch[1], i])
                state = 0

    return ''.join(out)