from python_framework import Service, ServiceMethod

import Guess, Match


@Service()
class GuessService:

    @ServiceMethod(requestClass=[str, Match.Match])
    def createModel(self, wordGuess, match):
        try:
            self.validator.guess.validateWordGuess(wordGuess, match)
            self.service.word.createOrUpdateByText(wordGuess)
            self.service.guessEvent.createValidGuess(wordGuess, userId=match.user.id, matchId=match.id)
        except Exception as exception:
            self.service.guessEvent.createInvalidGuess(wordGuess, userId=match.user.id, matchId=match.id)
            raise exception
        return self.persist(Guess.Guess(word=wordGuess, user=match.user, match=match))


    @ServiceMethod(requestClass=[Match.Match])
    def persist(self, model):
        return self.repository.guess.save(model)
