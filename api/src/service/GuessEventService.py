from python_framework import Service, ServiceMethod

import GuessEvent
from enumeration.GuessEventStatus import GuessEventStatus


@Service()
class GuessEventService:

    @ServiceMethod(requestClass=[str])
    def createInvalidGuess(self, wordGuess, userId=None, matchId=None):
        return self.emit(GuessEvent.GuessEvent(
            word = wordGuess,
            status = GuessEventStatus.INVALID,
            userId = userId,
            matchId = matchId
        ))


    @ServiceMethod(requestClass=[GuessEvent.GuessEvent])
    def createValidGuess(self, wordGuess, userId=None, matchId=None):
        self.emit(GuessEvent.GuessEvent(
            word = wordGuess,
            status = GuessEventStatus.VALID,
            userId = userId,
            matchId = matchId
        ))


    @ServiceMethod(requestClass=[GuessEvent.GuessEvent])
    def emit(self, event):
        return self.repository.guessEvent.save(event)
