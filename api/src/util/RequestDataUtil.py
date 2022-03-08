from python_helper import Constant as c

from constant import RequestDataConstant
from dto import RequestDataDto


COMBINED_IPV6_COMA_IPV4 = f'{RequestDataConstant.DEFAUTL_IPV6}, {RequestDataConstant.DEFAUTL_IPV4}'


def getIpv6(headers):
    return headers.get('Cf-Connecting-Ip', headers.get('X-Forwarded-For', f'{COMBINED_IPV6_COMA_IPV4}').split(c.COMA)[0])


def getIpv4(headers):
    return headers.get('X-Real-Ip', headers.get('X-Forwarded-For', f'{COMBINED_IPV6_COMA_IPV4}').split(c.COMA)[1])


def getUserAgent(headers):
    return f'''{headers.get('User-Agent', f'{RequestDataConstant.DEFAUTL_USER_AGENT}')}'''


def getUserAgentComplement(headers):
    return f'''{headers.get('Sec-Ch-Ua', f'{RequestDataConstant.DEFAUTL_USER_AGENT_COMPLEMENT}')}'''


def getPlataform(headers):
    return headers.get('Sec-Ch-Ua-Platform', f'{RequestDataConstant.DEFAUTL_PLATAFORM}')


def getDevice(headers):
    return headers.get('Sec-Ch-Ua-Mobile', f'{RequestDataConstant.DEFAUTL_DEVICE}').replace(c.QUESTION_MARK, c.BLANK)


def getCountry(headers):
    return headers.get('Cf-Ipcountry', f'{RequestDataConstant.DEFAUTL_COUNTRY}')


def getRequestDataRequestDto(headers):
    return RequestDataDto.RequestDataRequestDto(
        ipv6 = getIpv6(headers),
        ipv4 = getIpv4(headers),
        userAgent = getUserAgent(headers),
        userAgentComplement = getUserAgentComplement(headers),
        plataform = getPlataform(headers),
        device = getDevice(headers),
        country = getCountry(headers)
    )
