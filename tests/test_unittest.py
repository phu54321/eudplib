import profile_tool
import helper

DoCoverageTest = False

if DoCoverageTest:
    import coverage
    cov = coverage.Coverage()
    cov.start()


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
    test_eps,
    testshortcircuit,
    testlistloopcompiles,
    testmapdatahelper,
)

helper.CompressPayload(True)


def f():
    helper.test_runall('unittest')


# profile_tool.profile(f, 'profile.json')
f()

if DoCoverageTest:
    cov.stop()
    cov.html_report(include=["C:\\gitclones\\eudtrglib\\eudplib\\*"])
