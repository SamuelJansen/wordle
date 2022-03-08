from python_framework import Enum, EnumItem


@Enum()
class MatchContextEnumeration :
    ADMIN = EnumItem()
    USER = EnumItem()


MatchContext = MatchContextEnumeration()
