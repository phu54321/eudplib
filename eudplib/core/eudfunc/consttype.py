from ..rawtrigger import (
    EncodeAllyStatus,
    EncodeComparison,
    EncodeCount,
    EncodeModifier,
    EncodeOrder,
    EncodePlayer,
    EncodeProperty,
    EncodePropState,
    EncodeResource,
    EncodeScore,
    EncodeSwitchAction,
    EncodeSwitchState,
    EncodeAIScript,
    EncodeLocation,
    EncodeLocation,
    EncodeUnit,
    EncodeString,
    EncodeSwitch,
)


def createEncoder(f):
    class _:
        @staticmethod
        def cast(s):
            return f(s)
    return _


TrgAllyStatus = createEncoder(EncodeAllyStatus)
TrgComparison = createEncoder(EncodeComparison)
TrgCount = createEncoder(EncodeCount)
TrgModifier = createEncoder(EncodeModifier)
TrgOrder = createEncoder(EncodeOrder)
TrgPlayer = createEncoder(EncodePlayer)
TrgProperty = createEncoder(EncodeProperty)
TrgPropState = createEncoder(EncodePropState)
TrgResource = createEncoder(EncodeResource)
TrgScore = createEncoder(EncodeScore)
TrgSwitchAction = createEncoder(EncodeSwitchAction)
TrgSwitchState = createEncoder(EncodeSwitchState)
TrgAIScript = createEncoder(EncodeAIScript)
TrgLocation = createEncoder(EncodeLocation)
TrgString = createEncoder(EncodeString)
TrgSwitch = createEncoder(EncodeSwitch)
TrgUnit = createEncoder(EncodeUnit)
