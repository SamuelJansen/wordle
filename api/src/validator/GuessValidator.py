from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import Match


@Validator()
class GuessValidator:

    @ValidatorMethod(requestClass=[dict, Match.Match])
    def validateWordGuess(self, wordGuess, match):
        if ObjectHelper.isNone(wordGuess):
            raise GlobalException(
                logMessage = f'Word guess cannot be None',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )
        for guess in match.guessList:
            if guess.word == wordGuess:
                raise GlobalException(
                    message = f'Word already guessed',
                    logMessage = f'The word "{wordGuess}" already guessed. Word guess list: {[guess.word in match.guessList]}',
                    status = HttpStatus.BAD_REQUEST
                )
