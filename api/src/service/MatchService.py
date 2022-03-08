from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod, SessionManager

from constant import MatchConstant
from enumeration.MatchContext import MatchContext
from enumeration.MatchStep import MatchStep
import User, Match, Guess


@Service()
class MatchService:

    def abandon(self):

        findCurrentMatchByUserId(self.service.session.getContextId())

    @ServiceMethod(requestClass=[User.User])
    def findOrCreateModelByUserModel(self, user):
        model = self.findCurrentMatchByUserId(user.id)
        if ObjectHelper.isNone(model) or self.isNotValidMatch(model):
            model = Match.Match(
                user = user,
                context = self.service.session.getContext(
                    user.id,
                    [MatchContext.USER],
                    MatchConstant.DEFAULT_MATCH_TIME_IN_MINUTES
                ),
                word = self.service.word.getRandomWord(),
                totalGuesses = MatchConstant.DEFAUTL_TOTAL_GUESSES,
                step = MatchConstant.INITIAL_STEP
            )
        return self.fromModelToResponseDto(model)


    @ServiceMethod(requestClass=[User.User, str])
    def updateGuess(self, user, wordGuess):
        model = self.findCurrentMatchByUserId(user.id)
        guess = self.service.guess.createInvalidModel(wordGuess, user, model)
        self.service.word.validate(wordGuess)
        self.mapper.guess.overrideStatusToValidStatus(guess)
        if model.step not in MatchConstant.END_MATCH_STEP_LIST:
             model.step = MatchStep.GUESSING
        if wordGuess not in [guess.word for guess in model.guessList]:
            model.guessList.append(guess)
            if model.word == guess.word:
                model.step = MatchStep.VICTORY
        if len(self.helper.guess.getSortedValidGuessList(model.guessList)) > model.totalGuesses and model.step not in MatchConstant.END_MATCH_STEP_LIST:
            model.step = MatchStep.LOSS
        return self.fromModelToResponseDto(model)


    @ServiceMethod(requestClass=[int])
    def findCurrentMatchByUserId(self, userId):
        return self.repository.match.findMostRecentByUserIdAndStepIn(userId, MatchConstant.ONGOING_MATCH_STEP_LIST)


    @ServiceMethod(requestClass=[Match.Match])
    def isValidMatch(self, match):
        return self.service.session.isValidSession(match.context)


    @ServiceMethod(requestClass=[Match.Match])
    def isNotValidMatch(self, match):
        return not self.isValidMatch(match)


    @ServiceMethod(requestClass=[Match.Match])
    def persist(self, model):
        return self.repository.match.save(model)


    @ServiceMethod(requestClass=[Match.Match])
    def fromModelToResponseDto(self, model):
        return self.mapper.match.fromModelToResponseDto(self.persist(model))
