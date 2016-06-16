import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

import eudplib
eudftype = eudplib.core.varfunc.eudf.EUDFuncN

def varnames(f):
    if isinstance(f, eudftype):
        f = f._fdecl_func
    argcount = f.__code__.co_argcount
    return f.__code__.co_varnames[:argcount]

deflist = []
for name in eudplib.__all__:
    value = eudplib.__dict__[name]
    if name[:2] == 'f_':
        deflist.append("%s(%s)" % (name, ', '.join(varnames(value))))

deflist.sort()

for d in deflist:
    print(d)
