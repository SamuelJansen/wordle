from python_framework import Helper, HelperMethod

from enumeration.GuessStatus import GuessStatus
import Guess


@Helper()
class GuessHelper:

    @HelperMethod(requestClass=[[Guess.Guess]])
    def getSortedValidGuessList(self, guessList):
        return sorted([g for g in guessList if GuessStatus.VALID == g.status], key=lambda guess: guess.createdAt, reverse=False)
