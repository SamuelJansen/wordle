from python_framework import Service, ServiceMethod

from constant import MatchConstant
from enumeration.MatchContext import MatchContext
from dto import WordGuessDto


@Service()
class GameService:

    @ServiceMethod()
    def createContext(self):
        return self.service.session.createContext([MatchContext.USER], MatchConstant.DEFAULT_MATCH_TIME_IN_MINUTES)


    @ServiceMethod()
    def findOrCreateMatch(self):
        user = self.service.user.findOrCreateModel()
        return self.service.match.findOrCreateModelByUserModel(user)


    @ServiceMethod(requestClass=[WordGuessDto.WordGuessRequestParamDto])
    def updateGuess(self, paramRequestDto):
        user = self.service.user.findOrCreateModel()
        return self.service.match.updateGuess(user, paramRequestDto.word)


    @ServiceMethod()
    def abandonMatch(self):
        self.service.match.abandon()
