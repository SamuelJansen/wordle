from python_framework import SqlAlchemyProxy as sap
from python_framework import ConverterStatic

from ModelAssociation import MATCH, GUESS_EVENT, USER, MODEL
from util import AuditoryUtil, ModelUtil
from constant import GuessEventConstant
from enumeration.GuessEventStatus import GuessEventStatus


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class GuessEvent(MODEL):
    __tablename__ = GUESS_EVENT

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    word = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False)
    status = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False, default=GuessEventConstant.DEFAULT_STATUS)

    userId = sap.Column(sap.Integer())
    matchId = sap.Column(sap.Integer())

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        word = None,
        status = None,
        userId = None,
        matchId = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.word = word
        self.status = ConverterStatic.getValueOrDefault(GuessEventStatus.map(status), GuessEventConstant.DEFAULT_STATUS)
        self.userId = userId
        self.matchId = matchId
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, word: {self.word}, userId: {self.userId}, matchId: {self.matchId}, status: {self.status})'
