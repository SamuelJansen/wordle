from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


API_KEY = globalsInstance.getSetting('word.data.api-key')
RAPID_HOST = globalsInstance.getSetting('word.data.rapid-host')
BASE_URL = globalsInstance.getSetting('word.data.base-url')
DEFAULT_TIMEOUT_IN_SECONDS = globalsInstance.getSetting('word.data.default-timeout-in-seconds')
