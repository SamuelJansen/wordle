from python_framework import SessionManager
from python_helper import log


def getApiInstance(service):
    return service.globals.api


def isValidSession(service, jwtBody):
    isValid = False
    try:
        apiInstance = getApiInstance(service)
        apiInstance.sessionManager.validateAccessSession(apiInstance.sessionManager.decode(jwtBody))
        isValid = True
    except Exception as exception:
        log.debug(isValidSession, f'Invalid Session. Returnning "isValid={isValid}" by default', exception=exception)
    return isValid


def getIdentity(service):
    return SessionManager.getIdentity(apiInstance = getApiInstance(service))
