class RequestDataRequestDto:

    def __init__(self,
        id = None,
        ipv6 = None,
        ipv4 = None,
        userAgent = None,
        userAgentComplement = None,
        plataform = None,
        device = None,
        country = None
    ):
        self.id = id
        self.ipv6 = ipv6
        self.ipv4 = ipv4
        self.userAgent = userAgent
        self.userAgentComplement = userAgentComplement
        self.plataform = plataform
        self.device = device
        self.country = country


class RequestDataResponseDto:

    def __init__(self,
        id = None,
        ipv6 = None,
        ipv4 = None,
        userAgent = None,
        userAgentComplement = None,
        plataform = None,
        device = None,
        country = None
    ):
        self.id = id
        self.ipv6 = ipv6
        self.ipv4 = ipv4
        self.userAgent = userAgent
        self.userAgentComplement = userAgentComplement
        self.plataform = plataform
        self.device = device
        self.country = country
