from python_framework import Service, ServiceMethod, FlaskUtil

from util import RequestDataUtil
from dto import RequestDataDto
import RequestData


@Service()
class RequestDataService:

    def getRequestDataRequestDto(self):
        return RequestDataUtil.getRequestDataRequestDto(FlaskUtil.safellyGetHeaders())

    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def findOrCreateModelByRequestDto(self, dto, user=None):
        if self.notExistsByRequestDataRequestDto(dto):
            return self.createModel(dto, user=user)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def createModel(self, dto, user=None):
        return self.persist(self.mapper.requestData.fromRequestDtoToModel(dto, user=user))


    @ServiceMethod(requestClass=[RequestData.RequestData])
    def persist(self, model):
        return self.repository.requestData.save(model)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def existsByRequestDataRequestDto(self, dto):
        return self.repository.requestData.existsByRequestDataRequestDto(dto)


    @ServiceMethod(requestClass=[RequestDataDto.RequestDataRequestDto])
    def notExistsByRequestDataRequestDto(self, dto):
        return not self.existsByRequestDataRequestDto(dto)
