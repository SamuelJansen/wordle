from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

import Guess, Match
from dto import GuessDto, GuessStateDto, MatchDto
from enumeration.GuessState import GuessState


@Mapper()
class GuessMapper:

    @MapperMethod(requestClass=[[GuessDto.GuessRequestDto]], responseClass=[[Guess.Guess]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList


    @MapperMethod(requestClass=[[Guess.Guess]], responseClass=[[GuessDto.GuessResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[GuessDto.GuessRequestDto], responseClass=[Guess.Guess])
    def fromRequestDtoToModel(self, dto, model):
        return model


    @MapperMethod(requestClass=[Guess.Guess], responseClass=[GuessDto.GuessResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto


    @MapperMethod(requestClass=[Match.Match, MatchDto.MatchResponseDto])
    def overrideGuessStatesResponseDto(self, match, matchDto):
        matchDto.guessStates = [
            GuessStateDto.GuessStateRespopnseDto(
                id = guessRowIndex,
                guessStateRowList = [
                    GuessStateDto.GuessStateRowRespopnseDto(
                        id = letterIndex,
                        key = letter,
                        state = self.getLetterState(letter, match.word, letterIndex, isUnseen=guessRow.id<len(match.guessList))
                    ) for letterIndex, letter in enumerate(guessRow.word)
                ]
            ) for guessRowIndex, guessRow in enumerate(self.helper.guess.getSortedGuessList(match.guessList))
        ]


    @MapperMethod(requestClass=[str, str, int])
    def getLetterState(self, guessLetter, word, letterIndex, isUnseen=False):
        if isUnseen:
            return GuessState.UNSEEN
        if guessLetter == word[letterIndex]:
            return GuessState.CORRECT
        if guessLetter in word:
            return GuessState.CONTAIN
        else:
            return GuessState.INCORRECT
