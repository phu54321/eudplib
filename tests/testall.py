import helper
from simpletests import (
    # testperf,
    # testprint,

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
    teststruct2,
)

helper.CompressPayload(True)
helper.test_runall()
