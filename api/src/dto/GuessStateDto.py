from python_framework import ConverterStatic
from enumeration.GuessState import GuessState


class GuessStateRespopnseDto:
    def __init__(self,
        id = None,
        guessStateRowList = None
    ):
        self.id = id
        self.guessStateRowList = guessStateRowList

class GuessStateRowRespopnseDto:
    def __init__(self,
        id = None,
        key = None,
        state = None
    ):
        self.id = id
        self.key = key
        self.state = ConverterStatic.getValueOrDefault(GuessState.map(state), GuessState.UNKNOWN)
