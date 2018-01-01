DoCoverageTest = False

if DoCoverageTest:
    import coverage
    cov = coverage.Coverage()
    cov.start()

import helper


helper.EP_SetRValueStrictMode(True)


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
    testcpmemio,
    testptrmemio,
    testtypedf,
    testpool,
    test_lvalue,
    test_sq_from_1var,
    test_eps
)

helper.CompressPayload(True)
helper.test_runall('unittest')


if DoCoverageTest:
    cov.stop()
    cov.html_report(include=["C:\\gitclones\\eudtrglib\\eudplib\\*"])
