
"""
Useful utilities. You may freely use these functions.
"""

from eudtrg import LICENSE #@UnusedImport

def EPD(offset):
    """
    Converts normal address to EPD player.
    """
    return (offset - 0x0058A364) // 4


def FlattenList(l):
    ret = []
    try:
        for item in l:
            ret.extend(FlattenList(item))

    except TypeError: # l is not iterable
        ret.append(l)

    return ret
