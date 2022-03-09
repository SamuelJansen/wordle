from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.MatchContext import MatchContext
from dto import WordGuessDto, MatchDto


@Controller(url = '/api', tag='Match', description='Match controller')
class MatchController:

    @ControllerMethod(url = '/match/verify',
        requestParamClass = WordGuessDto.WordGuessRequestParamDto,
        contextRequired = [MatchContext.USER],
        responseClass = [MatchDto.MatchResponseDto]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, params=None):
        return self.service.game.updateGuess(params), HttpStatus.OK


    @ControllerMethod(url = '/match',
        contextRequired = [MatchContext.USER],
        responseClass = [MatchDto.MatchResponseDto]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self):
        return self.service.game.findOrCreateMatch(), HttpStatus.CREATED


    @ControllerMethod(url = '/match',
        contextRequired = [MatchContext.USER],
        responseClass = [MatchDto.MatchResponseDto]
        # , logRequest = True
        # , logResponse = True
    )
    def delete(self):
        return self.service.game.abandonMatch(), HttpStatus.DELETED
