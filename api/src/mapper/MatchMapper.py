from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

import Match
from dto import MatchDto, GuessStateDto

@Mapper()
class MatchMapper:

    @MapperMethod(requestClass=[[MatchDto.MatchRequestDto]], responseClass=[[Match.Match]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList


    @MapperMethod(requestClass=[[Match.Match]], responseClass=[[MatchDto.MatchResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[MatchDto.MatchRequestDto], responseClass=[Match.Match])
    def fromRequestDtoToModel(self, dto, model):
        return model


    @MapperMethod(requestClass=[Match.Match], responseClass=[MatchDto.MatchResponseDto])
    def fromModelToResponseDto(self, model, dto):
        self.mapper.guess.overrideGuessStatesResponseDto(model, dto)
        dto.wordSize = len(model.word)
        return dto
