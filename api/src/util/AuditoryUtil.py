from python_helper import log
from python_framework import SessionManager, ConverterStatic, JwtConstant

from constant import AuditoryConstant


def overrideSessionData(model):
    ConverterStatic.overrideData(
        model,
        ConverterStatic.getValueOrDefault(
            safellyGetCurrentSession().get(JwtConstant.KW_IDENTITY),
            AuditoryConstant.DEFAULT_USER
        )
    )


def safellyGetCurrentSession(apiInstance=None):
    currentSession = None
    try:
        currentSession = SessionManager.getCurrentSession(apiInstance=apiInstance)
    except Exception as exception:
        log.log(safellyGetCurrentSession, f'Not possible to get current session. Returning "{currentSession}" by default', exception=exception)
    return ConverterStatic.getValueOrDefault(currentSession, {})
