from python_framework import SqlAlchemyProxy as sap
from python_framework import ConverterStatic

from ModelAssociation import USER, MATCH, GUESS, MODEL
from util import AuditoryUtil, ModelUtil
from constant import MatchConstant
from config import MatchConfig
from enumeration.MatchStep import MatchStep


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class Match(MODEL):
    __tablename__ = MATCH

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    context = sap.Column(sap.String(GIANT_STRING_SIZE), nullable=False)
    word = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False)
    totalGuesses = sap.Column(sap.Integer(), nullable=False, default=MatchConfig.DEFAUTL_TOTAL_GUESSES)
    step = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False, default=MatchConstant.INITIAL_STEP)

    user, userId = sap.getManyToOne(MATCH, USER, MODEL)
    guessList = sap.getOneToMany(MATCH, GUESS, MODEL)

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        context = None,
        word = None,
        totalGuesses = None,
        step = None,
        user = None,
        userId = None,
        guessList = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.context = context
        self.word = word
        self.totalGuesses = totalGuesses
        self.step = ConverterStatic.getValueOrDefault(MatchStep.map(step), MatchStep.UNKNOWN)
        self.user, self.userId = ModelUtil.getManyToOneData(user, userId, MODEL)
        self.guessList = ModelUtil.getOneToManyData(guessList)
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, userId: {self.userId}, word: {self.word}, totalGuesses: {self.totalGuesses}, len(guessList): {len(self.guessList)})'
