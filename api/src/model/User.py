from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import REQUEST_DATA, USER, GUESS, MATCH, MODEL
from util import AuditoryUtil, ModelUtil
from constant import UserConstant


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class User(MODEL):
    __tablename__ = USER

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    name = sap.Column(sap.String(MEDIUM_STRING_SIZE), default=UserConstant.DEFAUTL_USER_NAME)

    requestDataList = sap.getOneToMany(USER, REQUEST_DATA, MODEL)
    matchList = sap.getOneToMany(USER, MATCH, MODEL)
    guessList = sap.getOneToMany(USER, GUESS, MODEL)

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        name = None,
        requestDataList = None,
        matchList = None,
        guessList = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.name = name
        self.requestDataList = ModelUtil.getOneToManyData(requestDataList)
        self.matchList = ModelUtil.getOneToManyData(matchList)
        self.guessList = ModelUtil.getOneToManyData(guessList)
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, name: {self.name}, len(requestDataList): {len(self.requestDataList)}, len(guessList): {len(self.guessList)})'
