from importlib.machinery import (
    FileFinder,
    SourceFileLoader,
)

from .epscompile import epsCompile
from eudplib.utils import EPError
import sys
import re
from bisect import bisect_right

import types


lineno_regex = re.compile(b' *# \\(Line (\\d+)\\) .+')


def modifyCodeLineno(codeobj, codeMap):
    co_lnotab = codeobj.co_lnotab
    co_firstlineno = codeobj.co_firstlineno

    # Reconstruct code data
    new_lnotab = []
    currentLine = co_firstlineno
    currentMappedLine = codeMap(currentLine)
    for i in range(0, len(co_lnotab), 2):
        bytecodeLen, lineAdvance = co_lnotab[i: i + 2]
        nextLine = currentLine + lineAdvance
        nextMappedLine = codeMap(nextLine)
        newLineAdvance = nextMappedLine - currentMappedLine
        while newLineAdvance >= 0xFF:
            new_lnotab.append(bytes([0, 0xFF]))
            newLineAdvance -= 0xFF
        new_lnotab.append(bytes([bytecodeLen, newLineAdvance]))
        currentLine = nextLine
        currentMappedLine = nextMappedLine

    # For code objects
    new_co_consts = []
    for c in codeobj.co_consts:
        if isinstance(c, types.CodeType):
            c = modifyCodeLineno(c, codeMap)
        new_co_consts.append(c)

    codeobj = types.CodeType(
        codeobj.co_argcount,
        codeobj.co_kwonlyargcount,
        codeobj.co_nlocals,
        codeobj.co_stacksize,
        codeobj.co_flags,
        codeobj.co_code,
        tuple(new_co_consts),
        codeobj.co_names,
        codeobj.co_varnames,
        codeobj.co_filename,
        codeobj.co_name,
        codeMap(co_firstlineno),  # codeobj.co_firstlineno,
        b''.join(new_lnotab),  # codeobj.co_lnotab,
        codeobj.co_freevars,
        codeobj.co_cellvars
    )

    return codeobj


class EPSLoader(SourceFileLoader):
    def get_data(self, path):
        """Return the data from path as raw bytes."""
        fileData = open(path, 'rb').read()
        if path.endswith('.pyc') or path.endswith('.pyo'):
            return fileData
        compiled = epsCompile(path, fileData)
        if compiled is None:
            raise EPError('epScript compiled failed for %s' % path)
        return compiled

    def source_to_code(self, data, path, *, _optimize=-1):
        codeobj = super().source_to_code(data, path, _optimize=_optimize)

        # Read lines from code data
        codeLine = [0]
        codeMap = [0]
        data = data.replace(b'\r\n', b'\n')
        for lineno, line in enumerate(data.split(b'\n')):
            match = lineno_regex.match(line)
            if match:
                codeLine.append(lineno + 1)
                codeMap.append(int(match.group(1)))

        # Reconstruct code data
        def lineMapper(line):
            return codeMap[bisect_right(codeLine, line) - 1]
        codeobj = modifyCodeLineno(codeobj, lineMapper)
        return codeobj


class EPSFinder:
    def __init__(self):
        self._finderCache = {}

    def _getFinder(self, path):
        try:
            return self._finderCache[path]
        except KeyError:
            self._finderCache[path] = FileFinder(path, (EPSLoader, ['.eps']))
            return self._finderCache[path]

    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path
        for pathEntry in path:
            finder = self._getFinder(pathEntry)
            spec = finder.find_spec(fullname)
            if spec is None:
                continue
            return spec


sys.meta_path.append(EPSFinder())
