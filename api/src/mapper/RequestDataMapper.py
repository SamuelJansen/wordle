from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

from util import ModelUtil
from dto import RequestDataDto
import RequestData


@Mapper()
class RequestDataMapper:

    @MapperMethod(requestClass=[[RequestDataDto.RequestDataRequestDto]], responseClass=[[RequestData.RequestData]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        return modelList


    @MapperMethod(requestClass=[[RequestData.RequestData]], responseClass=[[RequestDataDto.RequestDataResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList) :
        return dtoList


    @MapperMethod(requestClass=[RequestDataDto.RequestDataRequestDto], responseClass=[RequestData.RequestData])
    def fromRequestDtoToModel(self, dto, model, user=None):
        if ObjectHelper.isNotNone(user):
            model.user, model.userId = ModelUtil.getManyToOneData(user, user.id, user.__class__)
        return model


    @MapperMethod(requestClass=[RequestData.RequestData], responseClass=[RequestDataDto.RequestDataResponseDto])
    def fromModelToResponseDto(self, model, dto) :
        return dto
