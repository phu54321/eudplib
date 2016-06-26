import helper

'''
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
)
'''

from perftests import (
    testbasic,
)

helper.CompressPayload(True)
helper.test_runall('everything')
