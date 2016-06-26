import helper
from unittests import (
    testperf,
    testprint,

    testblockstru,
    testcurpl,
    testpatch,
    testarray,
    testptrigger,
    testptrjump,
    testswitch,
    testvartrg,
    testmultiret,
    testvarray,
    teststruct,
)

helper.CompressPayload(True)
helper.test_runall('unittest')
