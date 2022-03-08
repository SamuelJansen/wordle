from python_framework import Controller, ControllerMethod, HttpStatus

from dto import SessionDto


@Controller(url = '/api/match', tag='Security', description='Security controller')
class SessionController:

    @ControllerMethod(url = '/authenticate',
        responseClass = [SessionDto.SessionResponseDto]
        # , logRequest = True
        , logResponse = True
    )
    def post(self):
        return self.service.game.createContext(), HttpStatus.CREATED
