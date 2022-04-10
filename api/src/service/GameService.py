from python_framework import Service, ServiceMethod

from constant import MatchConstant
from config import MatchConfig
from enumeration.MatchContext import MatchContext
from dto import WordGuessDto


@Service()
class GameService:

    @ServiceMethod()
    def createContext(self):
        return self.service.session.createContext([MatchContext.USER], MatchConfig.DEFAULT_MATCH_TIME_IN_MINUTES)


    @ServiceMethod()
    def findOrCreateMatch(self):
        user = self.service.user.findOrCreateModel()
        return self.service.match.findOrCreateByUserModel(user)


    @ServiceMethod(requestClass=[WordGuessDto.WordGuessRequestParamDto])
    def addGuess(self, paramRequestDto):
        user = self.service.user.findOrCreateModel()
        return self.service.match.addGuess(user, paramRequestDto.word)


    @ServiceMethod()
    def abandonMatch(self):
        self.service.match.abandon()
