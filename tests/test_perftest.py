import helper


from perftests import (
    testbasic,
    testmemio,
)

# helper.CompressPayload(True)
helper.test_runall('perf')
