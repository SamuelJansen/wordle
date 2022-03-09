from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import Match


@Validator()
class GuessValidator:

    @ValidatorMethod(requestClass=[dict, Match.Match])
    def validateWordGuess(self, wordGuess, match):
        self.validateWordDataClientResponse(self.service.word.getWordData(wordGuess), wordGuess, match)


    @ValidatorMethod(requestClass=[dict, str, Match.Match])
    def validateWordDataClientResponse(self, wordDataClientResponse, wordGuess, match):
        if HttpStatus.BAD_REQUEST <= int(wordDataClientResponse.get('result_code', HttpStatus.INTERNAL_SERVER_ERROR)):
            self.service.guessEvent.createInvalidGuess(wordGuess, userId=match.user.id, matchId=match.id)
            raise GlobalException(
                message = f'This word does not exists',
                logMessage = f'The word "{wordGuess}" does not exists. Client message: {wordDataClientResponse.get("result_msg")}',
                status = HttpStatus.BAD_REQUEST
            )
        self.service.guessEvent.createValidGuess(wordGuess, userId=match.user.id, matchId=match.id)
        self.service.word.createOrUpdateByText(wordGuess)
