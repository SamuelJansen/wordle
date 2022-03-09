from python_helper import RandomHelper
from python_framework import Service, ServiceMethod, HttpStatus, GlobalException

from config import RandomWordConfig, MatchConfig
import Word


@Service()
class WordService:

    @ServiceMethod(requestClass=[str])
    def getWordData(self, word):
        return self.client.wordData.getWordData(word)


    @ServiceMethod(requestClass=[int, int])
    def getRandomWordTextList(self, amount, length):
        wordTextList = []
        try:
            wordTextList = self.client.randomWord.getRandomWordTextList(amount, length)
            self.createOrUpdateAll(wordTextList)
        except Exception as exception:
            wordTextList = [word.text for word in self.getRandomWordList(amount, length)]
        return wordTextList


    @ServiceMethod(requestClass=[int, int])
    def getRandomWordList(self, amount, length):
        return self.repository.word.getRandomWordList(amount, length)


    @ServiceMethod(requestClass=[str])
    def createOrUpdateByText(self, text):
        self.validator.word.validateWordText(text)
        return self.createOrUpdateAll([text.lower()])[0]


    @ServiceMethod()
    def getRandomWord(self):
        return RandomHelper.sample(self.getRandomWordTextList(
            RandomWordConfig.WORDS_PER_REQUEST,
            MatchConfig.WORD_LENGHT
        )).upper()


    @ServiceMethod(requestClass=[[str]])
    def createOrUpdateAll(self, wordTextList):
        lowerWordTextList = [w.lower() for w in wordTextList]
        exixtingModelList = self.repository.word.findAllByTextIn(lowerWordTextList)
        return self.repository.word.saveAll([
            * exixtingModelList,
            * [
                Word.Word(text=wordText) for wordText in lowerWordTextList if wordText not in [
                    model.text for model in exixtingModelList
                ]
            ]
        ])
