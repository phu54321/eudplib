import helper
from simpletests import (
    testarray,
    testblockstru,
    testcurpl,
    testpatch,
    testperf,
    testprint,
    testptrigger,
    testptrjump,
    testswitch,
    testvartrg
)

helper.CompressPayload(True)
helper.test_runall()
