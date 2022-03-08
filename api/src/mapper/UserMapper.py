from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

import User
from dto import UserDto

@Mapper()
class UserMapper:

    @MapperMethod(requestClass=[[UserDto.UserRequestDto]], responseClass=[[User.User]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        return modelList

    @MapperMethod(requestClass=[[User.User]], responseClass=[[UserDto.UserResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList) :
        return dtoList

    @MapperMethod(requestClass=[UserDto.UserRequestDto], responseClass=[User.User])
    def fromRequestDtoToModel(self, dto, model, requestData=None) :
        if ObjectHelper.isNone(requestData):
            return model
        model.requestDataList.append(requestData)
        return model

    @MapperMethod(requestClass=[User.User], responseClass=[UserDto.UserResponseDto])
    def fromModelToResponseDto(self, model, dto) :
        return dto
