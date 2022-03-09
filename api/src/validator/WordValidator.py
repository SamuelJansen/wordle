from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import Match


@Validator()
class WordValidator:

    @ValidatorMethod(requestClass=[dict])
    def validateWordText(self, wordText):
        self.validateWordDataClientResponse(self.service.word.getWordData(wordText), wordText)


    @ValidatorMethod(requestClass=[dict, str])
    def validateWordDataClientResponse(self, wordDataClientResponse, wordText):
        if HttpStatus.BAD_REQUEST <= int(wordDataClientResponse.get('result_code', HttpStatus.INTERNAL_SERVER_ERROR)):
            raise GlobalException(
                message = f'This word does not exists',
                logMessage = f'The word "{wordText}" does not exists. Client message: {wordDataClientResponse.get("result_msg")}',
                status = HttpStatus.BAD_REQUEST
            )
