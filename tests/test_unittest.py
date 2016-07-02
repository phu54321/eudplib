import helper


from unittests import (
    testblockstru,
    testcurpl,
    testpatch,
    testarray,
    testptrigger,
    testoperator,
    testptrjump,
    testfptr,
    testprint,
    testswitch,
    testvartrg,
    testmultiret,
    testvarray,
    teststruct,
    testmath,
    testbinsearch,
    teststack,
    testdwmemio,
)

# helper.CompressPayload(True)
helper.test_runall('unittest')
