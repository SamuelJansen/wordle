from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

import User, RequestData

@Repository(model = User.User)
class UserRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsById(self, id) :
        return self.repository.existsByIdAndCommit(id, self.model)

    def findById(self, id) :
        if self.existsById(id) :
            return self.repository.findByIdAndCommit(id, self.model)

    def notExistsById(self, id) :
        return not self.existsById(id)

    def save(self, model) :
        return self.repository.saveAndCommit(model)

    def saveAll(self, modelList):
        return self.repository.saveAllAndCommit(modelList)

    def deleteById(self, id):
        self.repository.deleteByIdAndCommit(id, self.model)

    def findAllByIdIn(self, idList) :
        modelList = self.repository.session.query(self.model).filter(self.model.id.in_(idList)).all()
        self.repository.session.commit()
        return modelList

    def findAllByRequestDataRequestDto(self, requestDataRequestDto):
        return self.repository.session.query(self.model).join(RequestData.RequestData).filter(
            sap.and_(
                sap.and_(
                    RequestData.RequestData.ipv6 == requestDataRequestDto.ipv6,
                    RequestData.RequestData.country == requestDataRequestDto.country
                ),
                sap.and_(
                    RequestData.RequestData.plataform == requestDataRequestDto.plataform,
                    RequestData.RequestData.device == requestDataRequestDto.device
                )
            )
        ).group_by(self.model.id).all()
