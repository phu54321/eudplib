DoCoverageTest = False


if DoCoverageTest:
    import coverage
    cov = coverage.Coverage()
    cov.start()

import pyximport
pyximport.install()

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
    testcpmemio,
)

helper.CompressPayload(True)
helper.test_runall('unittest')

if DoCoverageTest:
    cov.stop()
    cov.html_report(include=["C:\\gitclones\\eudtrglib\\eudplib\\*"])
