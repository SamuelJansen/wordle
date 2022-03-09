from enumeration.MatchStep import MatchStep


DEFAULT_CORRECT_WORD = 'good try'
ONGOING_MATCH_STEP_LIST = [
    MatchStep.STARTED,
    MatchStep.GUESSING
]
END_MATCH_STEP_LIST = [
    MatchStep.VICTORY,
    MatchStep.LOSS,
    MatchStep.TIMEOUT,
    MatchStep.ABANDONED
]
INITIAL_STEP = MatchStep.STARTED
