from .rawtrigger import (
    EncodeLocation,
    EncodeUnit,
    EncodeString,
    EncodeSwitch,
)


class MapLocation:
    @staticmethod
    def cast(s):
        return EncodeLocation(s)


class MapUnit:
    @staticmethod
    def cast(s):
        return EncodeUnit(s)


class MapString:
    @staticmethod
    def cast(s):
        return EncodeString(s)


class MapSwitch:
    @staticmethod
    def cast(s):
        return EncodeSwitch(s)
