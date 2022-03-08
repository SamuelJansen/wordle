from python_framework import Enum, EnumItem


@Enum()
class MatchStepEnumeration :
    STARTED = EnumItem()
    GUESSING = EnumItem()
    VICTORY = EnumItem()
    LOSS = EnumItem()
    TIMEOUT = EnumItem()
    ABANDONED = EnumItem()
    UNKNOWN = EnumItem()


MatchStep = MatchStepEnumeration()
