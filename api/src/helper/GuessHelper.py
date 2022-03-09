from python_framework import Helper, HelperMethod

import Guess


@Helper()
class GuessHelper:

    @HelperMethod(requestClass=[[Guess.Guess]])
    def getSortedGuessList(self, guessList):
        return sorted(guessList, key=lambda guess: guess.createdAt, reverse=False)
