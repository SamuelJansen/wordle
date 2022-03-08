class GuessRequestDto:
    def __init__(self,
        id = None,
        word = None
    ):
        self.id = id
        self.word = word


class GuessResponseDto:
    def __init__(self,
        id = None,
        word = None
    ):
        self.id = id
        self.word = word
