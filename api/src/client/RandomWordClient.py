from python_framework import HttpClient, HttpClientMethod

from constant import RapidApiConstant
from config import RandomWordConfig


@HttpClient(
    url = RandomWordConfig.BASE_URL,
    timeout = RandomWordConfig.DEFAULT_TIMEOUT_IN_SECONDS,
    headers = {
        RapidApiConstant.RAPID_API_HOST_HEADER_KEY: RandomWordConfig.RAPID_HOST,
        RapidApiConstant.RAPID_API_KEY_HEADER_KEY: RandomWordConfig.API_KEY
    }
)
class RandomWordClient :

    @HttpClientMethod(
        requestClass = [int, int]
        # , logRequest = True
        # , logResponse = True
    )
    def getRandomWordTextList(self, amount, length):
        return self.get(params={
            "count": str(amount),
            "wordLength": str(length)
        })
