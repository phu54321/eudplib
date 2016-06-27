import helper

from unittests import (
    testblockstru,
    testcurpl,
    testpatch,
    testarray,
    testptrigger,
    testptrjump,
    testprint,
    testswitch,
    testvartrg,
    testmultiret,
    testvarray,
    teststruct,
    testoperator,  # Takes a lot of time to compile.
    testatan2,
    testbinsearch,
)


'''
from perftests import (
    testbasic,
)
'''

# helper.CompressPayload(True)
helper.test_runall('everything')
