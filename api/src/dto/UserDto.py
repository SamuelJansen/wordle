class UserRequestDto:
    def __init__(self,
        id = None,
        name = None,
        requestDataList = None
    ):
        self.id = id
        self.name = name
        self.requestDataList = requestDataList


class UserResponseDto:
    def __init__(self,
        id = None,
        name = None
    ):
        self.id = id
        self.name = name
