from python_framework import SqlAlchemyProxy as sap
from python_framework import ConverterStatic

from ModelAssociation import MATCH, GUESS, USER, MODEL
from util import AuditoryUtil, ModelUtil


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class Guess(MODEL):
    __tablename__ = GUESS

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    word = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False)

    user, userId = sap.getManyToOne(GUESS, USER, MODEL)
    match, matchId = sap.getManyToOne(GUESS, MATCH, MODEL)

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        word = None,
        user = None,
        userId = None,
        match = None,
        matchId = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.word = word
        self.user, self.userId = ModelUtil.getManyToOneData(user, userId, MODEL)
        self.match, self.matchId = ModelUtil.getManyToOneData(match, matchId, MODEL)
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, word: {self.word}, userId: {self.userId}, matchId: {self.matchId})'
