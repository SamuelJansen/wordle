from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod, SessionManager

from constant import MatchConstant
from config import MatchConfig
from enumeration.MatchContext import MatchContext
from enumeration.MatchStep import MatchStep
import User, Match, Guess


@Service()
class MatchService:

    @ServiceMethod()
    def abandon(self):
        model = self.findCurrentMatchByUserId(self.service.session.getContextId())
        self.mapper.match.overrideStepToAbandoned(model)
        return self.persist(model)


    @ServiceMethod(requestClass=[User.User])
    def findOrCreateModelByUserModel(self, user):
        model = self.findCurrentMatchByUserId(user.id)
        if ObjectHelper.isNone(model) or self.isNotValidMatch(model):
            model = Match.Match(
                user = user,
                context = self.service.session.getContext(
                    user.id,
                    [MatchContext.USER],
                    MatchConfig.DEFAULT_MATCH_TIME_IN_MINUTES
                ),
                word = self.service.word.getRandomWord(),
                totalGuesses = MatchConfig.DEFAUTL_TOTAL_GUESSES,
                step = MatchConstant.INITIAL_STEP
            )
        return self.mapper.match.fromModelToResponseDto(self.persist(model))


    @ServiceMethod(requestClass=[User.User, str])
    def updateGuess(self, user, wordGuess):
        model = self.findCurrentMatchByUserId(user.id)
        self.validator.match.validateWordGuess(wordGuess, model)
        guess = self.service.guess.createModel(wordGuess, model)
        if guess not in model.guessList:
            model.guessList.append()
        if model.step not in MatchConstant.END_MATCH_STEP_LIST:
             model.step = MatchStep.GUESSING
        if model.word == wordGuess:
            model.step = MatchStep.VICTORY
        if len(model.guessList) > model.totalGuesses and model.step not in MatchConstant.END_MATCH_STEP_LIST:
            model.step = MatchStep.LOSS
        return self.mapper.match.fromModelToResponseDto(self.persist(model))


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
