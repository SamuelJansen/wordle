from python_framework import Serializer, HttpStatus, JwtConstant
from queue_manager_api import MessageEmitter, MessageEmitterMethod, MessageDto

from config import WordleQueueConfig


@MessageEmitter(
    url = WordleQueueConfig.EMITTER_URL,
    timeout = WordleQueueConfig.EMITTER_TIMEOUT,
    headers = {
        'Content-Type': 'application/json',
        JwtConstant.DEFAULT_JWT_API_KEY_HEADER_NAME: f'Bearer {WordleQueueConfig.QUEUE_API_KEY}'
    }
    , muteLogs = False
    # , logRequest = True
    # , logResponse = True
)
class WordleEmitter:

    @MessageEmitterMethod(
        queueKey = WordleQueueConfig.EMITTER_CREATE_WORD_QUEUE
        # , logRequest = True
        # , logResponse = True
        # requestClass=[MessageDto.MessageRequestDto, str],
        # responseClass=[MessageDto.MessageRequestDto]
    )
    def createWord(self, dto):
        return self.emit(body=dto)


    @MessageEmitterMethod(
        queueKey = WordleQueueConfig.EMITTER_CREATE_GUESS_QUEUE
        # , logRequest = True
        # , logResponse = True
        # requestClass=[MessageDto.MessageRequestDto, str],
        # responseClass=[MessageDto.MessageRequestDto]
    )
    def createGuess(self, dto):
        return self.emit(body=dto)
