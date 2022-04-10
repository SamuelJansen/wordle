from python_framework import HttpClient, HttpClientMethod

from constant import RapidApiConstant
from config import WordDataConfig


@HttpClient(
    url = WordDataConfig.BASE_URL,
    timeout = WordDataConfig.DEFAULT_TIMEOUT_IN_SECONDS,
    headers = {
        RapidApiConstant.RAPID_API_HOST_HEADER_KEY: WordDataConfig.RAPID_HOST,
        RapidApiConstant.RAPID_API_KEY_HEADER_KEY: WordDataConfig.API_KEY
    }
)
class WordDataClient :

    @HttpClientMethod(
        requestClass = [str]
        # , logRequest = True
        # , logResponse = True
    )
    def getWordData(self, word):
        return self.get(params={"entry":str(word)})
