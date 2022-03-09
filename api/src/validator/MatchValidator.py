from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import Match


@Validator()
class MatchValidator:

    @ValidatorMethod(requestClass=[dict, Match.Match])
    def validateWordGuess(self, wordGuess, model):
        if wordGuess in [guess.word for guess in model.guessList]:
            raise GlobalException(
                message = f'Try another word',
                logMessage = f'The word {wordGuess} was already checked',
                status = HttpStatus.BAD_REQUEST
            )
