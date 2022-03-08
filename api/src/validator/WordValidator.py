from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import User


@Validator()
class WordValidator:

    @ValidatorMethod(requestClass=[dict, str])
    def validateWordDataClientResponse(self, responseAsDictionary, word):
        if HttpStatus.BAD_REQUEST <= int(responseAsDictionary.get('result_code', HttpStatus.INTERNAL_SERVER_ERROR)):
            raise GlobalException(
                message = f'The "{word}" word does not exists',
                logMessage = responseAsDictionary.get('result_msg'),
                status = HttpStatus.BAD_REQUEST
            )
