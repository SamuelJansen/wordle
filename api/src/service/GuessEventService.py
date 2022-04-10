from python_framework import Service, ServiceMethod, EnumItem

import GuessEvent
from enumeration.GuessEventStatus import GuessEventStatus


@Service()
class GuessEventService:


    @ServiceMethod(requestClass=[str])
    def createInvalidGuessEvent(self, wordGuess, userId=None, matchId=None):
        return self.emitGuessCreationEvent(wordGuess, userId, matchId, GuessEventStatus.INVALID)


    @ServiceMethod(requestClass=[GuessEvent.GuessEvent])
    def createValidGuessEvent(self, wordGuess, userId=None, matchId=None):
        return self.emitGuessCreationEvent(wordGuess, userId, matchId, GuessEventStatus.VALID)


    @ServiceMethod(requestClass=[dict])
    def createModel(self, dto):
        return self.persist(
            GuessEvent.GuessEvent(
                word = dto.get('wordGuess'),
                userId = dto.get('userId'),
                matchId = dto.get('matchId'),
                status = dto.get('status')
            )
        )


    @ServiceMethod(requestClass=[str, int, int, EnumItem])
    def emitGuessCreationEvent(self, wordGuess, userId, matchId, status):
        return self.emitEvent(GuessEvent.GuessEvent(
            word = wordGuess,
            status = status,
            userId = userId,
            matchId = matchId
        ))


    @ServiceMethod(requestClass=[GuessEvent.GuessEvent])
    def emitEvent(self, event):
        return self.emitter.wordle.createGuess({
            'wordGuess': event.word,
            'userId': event.userId,
            'matchId': event.matchId,
            'status': event.status
        })


    @ServiceMethod(requestClass=[GuessEvent.GuessEvent])
    def persist(self, model):
        self.repository.guessEvent.save(model)
