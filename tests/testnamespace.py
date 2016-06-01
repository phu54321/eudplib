import sys
import os
import pprint as pp

sys.path.insert(0, os.path.abspath('..\\'))

import eudplib
eudftype = eudplib.core.varfunc.eudf.EUDFuncN


for name in eudplib.__all__:
    value = eudplib.__dict__[name]
    if isinstance(value, eudftype):
        print(name, value.size())

print(eudplib.GetEUDNamespace())
