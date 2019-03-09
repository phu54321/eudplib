from helper import *


@EUDTypedFunc([TrgLocation, TrgString])
def x(a, b):
    test_equality(
        "Location and strings can be used as a parameter",
        [a, b],
        [EncodeLocation("Anywhere"), EncodeString("Hello world!")],
    )


@TestInstance
def test_mdhelper():
    assert TrgLocation.cast("Anywhere") == 64
    assert TrgString.cast("Hello world!") == EncodeString("Hello world!")
    assert TrgSwitch.cast("Switch 1") == 0
    assert TrgUnit.cast("Terran Marine") == 0
    x("Anywhere", "Hello world!")
