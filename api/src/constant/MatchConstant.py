from enumeration.MatchStep import MatchStep


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
