from python_framework import Service, ServiceMethod, EnumItem, SessionManager

from util import SessionManagerUtil
from dto import SessionDto


@Service()
class SessionService:

    @ServiceMethod(requestClass=[[EnumItem], int])
    def createContext(self, contextList, minutes):
        user = self.service.user.findOrCreateModel()
        return SessionDto.SessionResponseDto(
            context = self.getContext(user.id, contextList, minutes)
        )


    @ServiceMethod(requestClass=[int, [EnumItem], int])
    def getContext(self, id, contextList, minutes):
        return SessionManager.createAccessToken(
            id,
            contextList,
            deltaMinutes = minutes,
            apiInstance = SessionManagerUtil.getApiInstance(self)
        )


    @ServiceMethod(requestClass=[dict])
    def isValidSession(self, contextBody):
        return SessionManagerUtil.isValidSession(self, contextBody)


    @ServiceMethod(requestClass=[dict])
    def getContextId(self):
        return SessionManagerUtil.getIdentity(self)
