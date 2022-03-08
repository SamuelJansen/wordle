from python_framework import Service, ServiceMethod

import User, Guess, Match
from enumeration.GuessStatus import GuessStatus


@Service()
class GuessService:

    @ServiceMethod(requestClass=[str, User.User, Match.Match])
    def createInvalidModel(self, wordGuess, user, match):
        return self.persist(Guess.Guess(word=wordGuess, status=GuessStatus.INVALID, user=user, match=match))


    @ServiceMethod(requestClass=[Guess.Guess])
    def overrideToValidModel(model):
        model.status = GuessStatus.VALID


    @ServiceMethod(requestClass=[Guess.Guess])
    def persist(self, model):
        return self.repository.guess.save(model)
