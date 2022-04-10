from python_framework import Service, ServiceMethod, FlaskUtil
from python_helper import ObjectHelper

from dto import UserDto, RequestDataDto
import User, RequestData
from util import RequestDataUtil


@Service()
class UserService:

    @ServiceMethod()
    def findOrCreateModel(self):
        return self.persist(self.findOrCreateModelByRequestDataRequestDto(
            self.service.requestData.getRequestDataRequestDto()
        ))


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def notExistsByRequestDataRequestDto(self, requestDataRequestDto):
        return not self.existsByRequestDataRequestDto(requestDataRequestDto)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def existsByRequestDataRequestDto(self, requestDataRequestDto):
        return self.repository.user.existsByRequestDataRequestDto(requestDataRequestDto)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def createModelByRequestDataRequestDto(self, requestDataRequestDto):
        return self.createModel(UserDto.UserRequestDto(
            name = None,
            requestDataList = [requestDataRequestDto]
        ))


    @ServiceMethod(requestClass=[UserDto.UserRequestDto])
    def createModel(self, dto):
        return self.persist(self.mapper.user.fromRequestDtoToModel(dto))


    @ServiceMethod(requestClass=[User.User])
    def persist(self, model):
        return self.repository.user.save(model)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def findOrCreateModelByRequestDataRequestDto(self, requestDataRequestDto):
        modelList = self.repository.user.findAllByRequestDataRequestDto(requestDataRequestDto)
        if 0 == len(modelList):
            return self.createModelByRequestDataRequestDto(requestDataRequestDto)
        self.validator.user.validateOnlyOneUserWasFound(modelList)
        return modelList[0]
