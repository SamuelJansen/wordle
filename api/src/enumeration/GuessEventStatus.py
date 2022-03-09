from python_framework import Enum, EnumItem


@Enum()
class GuessEventStatusEnumeration :
    VALID = EnumItem()
    INVALID = EnumItem()
    UNKNOWN = EnumItem()


GuessEventStatus = GuessEventStatusEnumeration()
