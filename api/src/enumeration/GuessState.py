from python_framework import Enum, EnumItem


@Enum()
class GuessStateEnumeration :
    UNSEEN = EnumItem()
    CORRECT = EnumItem()
    CONTAIN = EnumItem()
    INCORRECT = EnumItem()
    UNKNOWN = EnumItem()


GuessState = GuessStateEnumeration()
