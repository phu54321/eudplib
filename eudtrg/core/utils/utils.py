import collections


def FlattenList(l):
    if type(l) is bytes or type(l) is str:
        return [l]

    try:
        ret = []
        for item in l:
            ret.extend(FlattenList(item))
        return ret

    except TypeError:  # l is not iterable
        return [l]


def EPD(p):
    return (p - 0x58A364) // 4


# -------

def List2Assignable(l):
    if len(l) == 1:
        return l[0]

    else:
        return l


def Assignable2List(a):
    if a is None:
        return []

    elif isinstance(a, collections.Iterable):
        return list(a)

    else:
        return [a]


# -------

# Original code from TrigEditPlus::ConvertString_SCMD2ToRaw

def SCMD2Text(b):
    b = b + b'\0'  # zero terminate

    output = []
    i = 0

    def toxdigit(i):
        if b'0'[0] <= i <= b'9'[0]:
            return i - 48
        elif b'a'[0] <= i <= b'z'[0]:
            return i - 97 + 10
        elif b'A'[0] <= i <= b'Z'[0]:
            return i - 65 + 10
        else:
            return None

    while i < len(b):
        if b[i:i + 2] == b'\\<'[0]:
            output.append('<')
            i += 2

        elif b[i:i + 2] == b'\\>'[0]:
            output.append('>')
            i += 2

        elif b[i:i + 3] == b'<R>'[0]:
            output.append(b'\x12')
            i += 3

        elif b[i:i + 3] == b'<C>'[0]:
            output.append(b'\x13')
            i += 3

        elif (
            b[i] == b'<'[0] and
            toxdigit(b[i + 1]) is not None and
            b[i + 2] == b'>'[0]
        ):
            output.append(bytes((
                toxdigit(b[i + 1]),
            )))
            i += 3

        elif (
            b[i] == b'<'[0] and
            toxdigit(b[i + 1]) is not None and
            toxdigit(b[i + 2]) is not None and
            b[i + 3] == b'>'[0]
        ):
            output.append(bytes((
                (toxdigit(b[i + 1]) << 4) | toxdigit(b[i + 2]),
            )))
            i += 4

        elif b[i] == '\r':
            i += 1

        else:
            output.append(bytes((b[i],)))
            i += 1

    return b''.join(output)
