from python_helper import ObjectHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

import Match

@Repository(model = Match.Match)
class MatchRepository:

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
        

    def findMostRecentByUserIdAndStepIn(self, userId, stepList):
        if ObjectHelper.isNone(userId) or ObjectHelper.isEmpty(stepList):
            return None
        model = self.repository.session.query(self.model).filter(
            sap.and_(
                self.model.userId == userId,
                self.model.step.in_(stepList)
            )
        ).order_by(self.model.createdAt.desc()).first()
        self.repository.session.commit()
        return model
