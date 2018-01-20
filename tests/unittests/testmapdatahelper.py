from helper import *


@EUDTypedFunc([MapLocation, MapString])
def x(a, b):
    test_equality(
        "Location and strings can be used as a parameter",
        [a, b],
        [EncodeLocation("Anywhere"), EncodeString("Hello world!")]
    )


@TestInstance
def test_mdhelper():
    assert MapLocation.cast("Anywhere") == 64
    assert MapString.cast("Hello world!") == EncodeString("Hello world!")
    assert MapSwitch.cast("Switch 1") == 0
    assert MapUnit.cast("Terran Marine") == 0
    x("Anywhere", "Hello world!")
