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
        return self.createOrUpdateAll([text])[0]


    @ServiceMethod()
    def getRandomWord(self):
        return RandomHelper.sample(self.getRandomWordTextList(
            RandomWordConfig.WORDS_PER_REQUEST,
            MatchConfig.WORD_LENGTH
        )).upper()


    @ServiceMethod(requestClass=[[str]])
    def createOrUpdateByTextListEvent(self, textList):
        return self.emitter.wordle.createWord({
            'wordList': textList
        })


    @ServiceMethod(requestClass=[[str]])
    def createOrUpdateAll(self, wordTextList):
        lowerWordTextList = [w.lower() for w in set(wordTextList)]
        exixtingModelList = self.repository.word.findAllByTextIn(lowerWordTextList)
        return self.repository.word.saveAll([
            * exixtingModelList,
            * [
                Word.Word(text=wordText, length=len(wordText)) for wordText in lowerWordTextList if wordText not in [
                    model.text for model in exixtingModelList
                ]
            ]
        ])
