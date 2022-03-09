class MatchRequestDto:
    def __init__(self,
        id = None,
        context = None,
        totalGuesses = None,
        user = None,
        userId = None
    ):
        self.id = id
        self.context = context
        self.totalGuesses = totalGuesses
        self.user = user
        self.guessList = guessList


class MatchResponseDto:
    def __init__(self,
        id = None,
        context = None,
        wordSize = None,
        totalGuesses = None,
        step = None,
        user = None,
        guessList = None,
        guessStates = None,
        correctWord = None
    ):
        self.id = id
        self.context = context
        self.wordSize = wordSize
        self.totalGuesses = totalGuesses
        self.step = step
        self.user = user
        self.guessList = guessList
        self.guessStates = guessStates
        self.correctWord = correctWord
