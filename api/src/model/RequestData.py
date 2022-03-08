from python_framework import SqlAlchemyProxy as sap

from ModelAssociation import REQUEST_DATA, USER, MODEL
from util import AuditoryUtil, ModelUtil
from constant import RequestDataConstant


GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64


class RequestData(MODEL):
    __tablename__ = REQUEST_DATA

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    ipv6 = sap.Column(sap.String(MEDIUM_STRING_SIZE), default=RequestDataConstant.DEFAUTL_IPV6)
    ipv4 = sap.Column(sap.String(LITTLE_STRING_SIZE), default=RequestDataConstant.DEFAUTL_IPV4)
    userAgent = sap.Column(sap.String(LARGE_STRING_SIZE), default=RequestDataConstant.DEFAUTL_USER_AGENT)
    userAgentComplement = sap.Column(sap.String(STRING_SIZE), default=RequestDataConstant.DEFAUTL_USER_AGENT_COMPLEMENT)
    plataform = sap.Column(sap.String(LITTLE_STRING_SIZE), default=RequestDataConstant.DEFAUTL_PLATAFORM)
    device = sap.Column(sap.String(LITTLE_STRING_SIZE), default=RequestDataConstant.DEFAUTL_DEVICE)
    country = sap.Column(sap.String(LITTLE_STRING_SIZE), default=RequestDataConstant.DEFAUTL_COUNTRY)

    user, userId = sap.getManyToOne(REQUEST_DATA, USER, MODEL)

    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    createdBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    updatedBy = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)

    def __init__(self,
        id = None,
        ipv6 = None,
        ipv4 = None,
        userAgent = None,
        userAgentComplement = None,
        plataform = None,
        device = None,
        country = None,
        user = None,
        userId = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.ipv6 = ipv6
        self.ipv4 = ipv4
        self.userAgent = userAgent
        self.userAgentComplement = userAgentComplement
        self.plataform = plataform
        self.device = device
        self.country = country
        self.user, self.userId = ModelUtil.getManyToOneData(user, userId, MODEL)
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideSessionData(self)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, userId: {self.userId}, ipv6: {self.ipv6}, ipv4: {self.ipv4}, plataform: {self.plataform}, device: {self.device}, country: {self.country})'
