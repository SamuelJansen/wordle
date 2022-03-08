from python_framework import HttpClient, HttpClientMethod

from constant import RapitApiConstant
from config import RandomWordConfig


@HttpClient(
    url = RandomWordConfig.BASE_URL,
    timeout = RandomWordConfig.DEFAULT_TIMEOUT_IN_SECONDS,
    headers = {
        RapitApiConstant.RAPID_API_HOST_HEADER_KEY: RandomWordConfig.RAPID_HOST,
        RapitApiConstant.RAPID_API_KEY_HEADER_KEY: RandomWordConfig.API_KEY
    }
)
class RandomWordClient :

    @HttpClientMethod(
        requestClass = [int, int]
    )
    def getRandomWordTextList(self, amount, size):
        return self.get(params={
            "count": str(amount),
            "wordLength": str(size)
        })
