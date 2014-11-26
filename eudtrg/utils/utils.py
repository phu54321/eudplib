def FlattenList(l):
    try:
        ret = []
        for item in l:
            ret.append(FlattenList(item))
        return ret

    except TypeError:
        return l


def EPD(p):
    return (p - 0x58A364) // 4
