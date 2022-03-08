from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import User


@Validator()
class UserValidator:

    @ValidatorMethod(requestClass=[[User.User]])
    def validateOnlyOneUserWasFound(self, modelList):
        if not len(modelList) == 1:
            raise GlobalException(
                logMessage = f'More than one user was found. User id list: {[mode.id for mode in modelList]}', 
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )
