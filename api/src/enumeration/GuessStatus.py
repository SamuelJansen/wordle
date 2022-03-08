from python_framework import Enum, EnumItem


@Enum()
class GuessStatusEnumeration :
    VALID = EnumItem()
    INVALID = EnumItem()
    UNKNOWN = EnumItem()


GuessStatus = GuessStatusEnumeration()
