from python_framework import Controller, ControllerMethod, HttpStatus

from dto import SessionDto


@Controller(url = '/api', tag='Security', description='Security controller')
class SessionController:

    @ControllerMethod(url = '/match/authenticate',
        responseClass = [SessionDto.SessionResponseDto]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self):
        return self.service.game.createContext(), HttpStatus.CREATED
