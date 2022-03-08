from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


API_KEY = globalsInstance.getSetting('word.random.api-key')
RAPID_HOST = globalsInstance.getSetting('word.random.rapid-host')
BASE_URL = globalsInstance.getSetting('word.random.base-url')
DEFAULT_TIMEOUT_IN_SECONDS = globalsInstance.getSetting('word.random.default-timeout-in-seconds')
WORDS_PER_REQUEST = globalsInstance.getSetting('word.random.words-per-request')
