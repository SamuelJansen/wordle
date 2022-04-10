from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


QUEUE_API_KEY = globalsInstance.getSetting('queue.wordle.api-key')

LISTENER_TIMEOUT = globalsInstance.getSetting('queue.wordle.listener.timeout')

EMITTER_URL = globalsInstance.getSetting('queue.wordle.emitter.url')
EMITTER_TIMEOUT = globalsInstance.getSetting('queue.wordle.emitter.timeout')

EMITTER_CREATE_WORD_QUEUE = globalsInstance.getSetting('queue.wordle.emitter.queue-key.create-word')
EMITTER_CREATE_GUESS_QUEUE = globalsInstance.getSetting('queue.wordle.emitter.queue-key.create-guess')
