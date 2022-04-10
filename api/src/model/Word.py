from python_framework import ConverterStatic
from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import WORD, MODEL
from constant import WordConstant
from util import AuditoryUtil


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class Word(MODEL):
    __tablename__ = WORD

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    text = sap.Column(sap.String(LITTLE_STRING_SIZE), nullable=False, unique=True)
    length = sap.Column(sap.Integer(), nullable=False, default=WordConstant.DEFAULT_LENGTH)

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        text = None,
        length = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.text = text
        self.length = ConverterStatic.getValueOrDefault(length, ConverterStatic.getValueOrDefault(len(text), WordConstant.DEFAULT_LENGTH))
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, text: {self.text}, length: {self.length})'
