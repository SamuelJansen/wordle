from python_helper import ObjectHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

import RequestData

@Repository(model = RequestData.RequestData)
class RequestDataRepository:

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

    def existsByRequestDataRequestDto(self, dto):
        exists = False
        if ObjectHelper.isNotNone(dto):
            exists = self.repository.session.query(sap.exists().where(
                sap.and_(
                    sap.and_(
                        sap.and_(
                            self.model.ipv4 == dto.ipv4,
                            self.model.ipv6 == dto.ipv6
                        ),
                        sap.and_(
                            self.model.country == dto.country,
                            True == True
                        )
                    ),
                    sap.and_(
                        sap.and_(
                            self.model.userAgent == dto.userAgent,
                            self.model.userAgentComplement == dto.userAgentComplement
                        ),
                        sap.and_(
                            self.model.plataform == dto.plataform,
                            self.model.device == dto.device
                        )
                    )
                )
            )).one()[0]
            self.repository.session.commit()
        return exists
