from ctypes import (
    CDLL,
    c_int, c_char_p,
)

from eudplib.utils import (
    u2b, find_data_file
)

libeps = CDLL(find_data_file('libepScriptLib.dll', __file__))
libeps.compileString.argtypes = [c_char_p, c_char_p]
libeps.freeCompiledResult.argtypes = [c_int]


def epsCompile(modname, bCode):
    modname = u2b(modname)
    output = libeps.compileString(modname, bCode)
    if not output:
        return None
    outputStr = c_char_p(output).value
    libeps.freeCompiledResult(output)
    return outputStr
