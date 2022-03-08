from python_helper import RandomHelper
from python_framework import Service, ServiceMethod, HttpStatus, GlobalException

from config import RandomWordConfig, MatchConfig
import Word


@Service()
class WordService:

    @ServiceMethod(requestClass=[str])
    def validate(self, word):
        wordDataClientResponse = self.client.wordData.getWordData(word)
        self.validator.word.validateWordDataClientResponse(wordDataClientResponse, word)


    @ServiceMethod(requestClass=[str])
    def validateAndCreateOrUpdateByText(self, word):
        self.validate(word)
        return self.createOrUpdateByText(word)


    @ServiceMethod(requestClass=[int, int])
    def getRandomWordTextList(self, amount, size):
        return self.client.randomWord.getRandomWordTextList(amount, size)


    @ServiceMethod(requestClass=[str])
    def createOrUpdateByText(self, text):
        return self.createAll([text.lower()])[0]


    @ServiceMethod()
    def getRandomWord(self):
        return RandomHelper.sample(self.createAll(self.getRandomWordTextList(
            RandomWordConfig.WORDS_PER_REQUEST,
            MatchConfig.WORD_LENGHT
        ))).text.upper()


    @ServiceMethod(requestClass=[[str]])
    def createAll(self, wordTextList):
        lowerWordTextList = [w.lower() for w in wordTextList]
        return self.repository.word.saveAll([
            Word.Word(text=wordText) for wordText in lowerWordTextList if wordText not in [
                model.text for model in self.repository.word.findAllByTextIn(lowerWordTextList)
            ]
        ])
