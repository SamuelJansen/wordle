from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()


DEFAULT_MATCH_TIME_IN_MINUTES = globalsInstance.getSetting('match.duration-in-minutes')
DEFAUTL_TOTAL_GUESSES = globalsInstance.getSetting('match.total-guesses')
WORD_LENGTH = globalsInstance.getSetting('match.word-length')
