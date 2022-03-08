const guessDisplay = document.querySelector('.guess-container')
const keyboard = document.querySelector('.keyboard-container')
const messageDisplay = document.querySelector('.message-container')

const WORDLE_API_BASE_URL = `${document.URL}/api`
const DEFAULT_REQUEST_TIMEOUT = 5000
const DEFAULT_ANIMATION_TIMEOUT = 200
const DEFAULT_MESSAGE_TIME_DURATIONT = 5000
const HEADER_SESSION_KEY = 'Context'
const DEFAULT_UX_ERROR_MESSAGE = 'An error occurred. Try again later'
const DEFAULT_HEADERS = new Headers({
    'Accept': 'application/body',
    'Content-Type': 'application/body',
    'Access-Control-Allow-Origin': '*'
});

const ENTER_KEY = 'ENTER'
const DELETE_KEY = '«'
const keyboardLineData = [
    [
        {'key': 'Q', 'relatedKeys': []},
        {'key': 'W', 'relatedKeys': []},
        {'key': 'E', 'relatedKeys': []},
        {'key': 'R', 'relatedKeys': []},
        {'key': 'T', 'relatedKeys': []},
        {'key': 'Y', 'relatedKeys': []},
        {'key': 'U', 'relatedKeys': []},
        {'key': 'I', 'relatedKeys': []},
        {'key': 'O', 'relatedKeys': []},
        {'key': 'P', 'relatedKeys': []}
    ],
    [
        {'key': 'A', 'relatedKeys': []},
        {'key': 'S', 'relatedKeys': []},
        {'key': 'D', 'relatedKeys': []},
        {'key': 'F', 'relatedKeys': []},
        {'key': 'G', 'relatedKeys': []},
        {'key': 'H', 'relatedKeys': []},
        {'key': 'J', 'relatedKeys': []},
        {'key': 'K', 'relatedKeys': []},
        {'key': 'L', 'relatedKeys': []}
    ],
    [
        {'key': ENTER_KEY, 'relatedKeys': []},
        {'key': 'Z', 'relatedKeys': []},
        {'key': 'X', 'relatedKeys': []},
        {'key': 'C', 'relatedKeys': []},
        {'key': 'V', 'relatedKeys': []},
        {'key': 'B', 'relatedKeys': []},
        {'key': 'N', 'relatedKeys': []},
        {'key': 'M', 'relatedKeys': []},
        {'key': DELETE_KEY, 'relatedKeys': []}
    ]
]
const guessDataRows = [
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '']
]
let wordSize = null
let totalGuesses = null
let currentGuessRowIndex = null
let currentGuessLetterIndex = null
let gameIsOver = null

let wordle = 'ABCDE'

const toggleFullScreen = () => {
  if (!document.fullscreenElement &&    // alternative standard method
      !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    } else if (document.documentElement.msRequestFullscreen) {
      document.documentElement.msRequestFullscreen();
    } else if (document.documentElement.mozRequestFullScreen) {
      document.documentElement.mozRequestFullScreen();
    } else if (document.documentElement.webkitRequestFullscreen) {
      document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
}

const fetchWithTimeout = (url, options={}) => {
    const { timeout = DEFAULT_REQUEST_TIMEOUT } = options
    const { handler = null } = options
    return Promise.race([
        fetch(url, options),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timeout')), timeout)
        )
    ])
        // .catch(error => handler())
}

const showUxErrorMessage = (enhancedResponse) => {
    if (500 > enhancedResponse.status) {
        return showMessage(enhancedResponse.body.message)
    }
    return showMessage(DEFAULT_UX_ERROR_MESSAGE)
}

const getBodyPromisse = (response) => {
    return ((r) => r.json())(response)
        .then(body => {
            return {
                response: response,
                status: response.status,
                body: body
            }
        })
        .then(enhancedResponse => {
            if (400 <= enhancedResponse.status) {
                showUxErrorMessage(enhancedResponse)
            }
            return enhancedResponse.body
        })
        .catch(error => {
            // console.log('Not possible to get response body properly because of the following exception')
            console.log(error)
        })

}

const showInternalErrorMessage = (error) => {
    console.log(error)
    if (!error.message) {
        console.log(`No message present. error.message: ${error.message}`)
    }
}

const updateContextHeader = () => {
    return fetchWithTimeout(`${WORDLE_API_BASE_URL}/match/authenticate`,
        {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            handler: updateContextHeader
        }
    )
        .then(response => getBodyPromisse(response))
        .then(body => {
            DEFAULT_HEADERS.delete(HEADER_SESSION_KEY)
            DEFAULT_HEADERS.append(HEADER_SESSION_KEY, `Bearer ${body.context}`)
            return body
        })
        .catch(error => showInternalErrorMessage(error))
}

const getInitialState = () => {
    return fetchWithTimeout(`${WORDLE_API_BASE_URL}/match`,
        {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            handler: getInitialState
        }
    )
        .then(response => getBodyPromisse(response))
        .catch(error => showInternalErrorMessage(error))
}

const resetIfNeeded = () => {
    wordSize = 5
    totalGuesses = 5
    currentGuessRowIndex = 0
    currentGuessLetterIndex = 0
    gameIsOver = false
    updateContextHeader()
        .then((_) => getInitialState())
        .then((body) => {
            wordSize = body.wordSize
            totalGuesses = body.totalGuesses
            return body
        })
        .then((body) => body.guessStates)
        .then((initialState) => {
            guessDataRows.forEach((guessRowContent, guessRowIndex) => {
                oldGuessRow = document.querySelector('#guess-row-' + guessRowIndex)
                if (oldGuessRow) {
                    oldGuessRow.remove()
                }
            })
            keyboardLineData.forEach((item, i) => {
                oldKeyboardLine = document.querySelector('.keyboard-line-container')
                if (oldKeyboardLine) {
                    oldKeyboardLine.remove()
                }
            });
            guessDataRows.forEach((guessRowContent, guessRowIndex) => {
                const guessRow = document.createElement('div')
                guessRow.setAttribute('id', 'guess-row-' + guessRowIndex)
                guessRowContent.forEach((guess, guessIndex) => {
                    const guessLetter = document.createElement('div')
                    guessLetter.setAttribute('id', 'guess-row-' + guessRowIndex + '-guess-letter-' + guessIndex)
                    guessLetter.classList.add('guess-letter')
                    guessRow.append(guessLetter)
                })
                guessDisplay.append(guessRow)
            })
            keyboardLineData.forEach((keyDataLine, keyDataLineIndex) => {
                const keyboardLine = document.createElement('div')
                keyboardLine.classList.add('keyboard-line-container')
                keyDataLine.forEach((keyData, keyDataIndex) => {
                    const buttonElement = document.createElement('button')
                    buttonElement.textContent = keyData.key
                    buttonElement.setAttribute('id', keyData.key)
                    buttonElement.addEventListener('click', () => handleClick(keyData.key))
                    keyboardLine.append(buttonElement)
                });
                keyboard.append(keyboardLine)
            })
            initialState.forEach((guess, guessIndex) => {
                guess.guessStateRowList.forEach((guessLetter, guessLetterIndex) => {
                    guessDataRows[guess.id][guessLetter.id] = guessLetter.key
                    guessElementLetter = findGuessElementLetterByRowIndexAndLetterIndex(guess.id, guessLetter.id)
                    guessElementLetter.textContent = guessLetter.key
                    guessElementLetter.setAttribute('typed-letter', guessLetter.key)
                });
            });
            currentGuessRowIndex = initialState.length
            flipAllGuessLetters(initialState)
        })


}

const checkRow = () => {
    const wordGuess = guessDataRows[currentGuessRowIndex].join('')
    let currentResponse = null
    if (currentGuessLetterIndex >= wordSize) {
        return fetch(`${WORDLE_API_BASE_URL}/match/verify?word=${wordGuess}`, {
            method: 'GET',
            headers: DEFAULT_HEADERS
        })
            .then((response) => {
                currentResponse = response
                return getBodyPromisse(response)
            })
            .then(body => {
                if (400 <= currentResponse.status) {
                    if (400 < currentResponse.status){
                        resetIfNeeded()
                    }
                    return
                }
                body.guessStates.forEach((guess, guessIndex) => {
                    if (currentGuessRowIndex == guess.id) {
                        flipGuessLetters(guess.guessStateRowList, guess.id)
                        if (body.step == 'VICTORY') {
                            gameIsOver = true
                            showMessage('Perfect!')
                                .then(() => resetIfNeeded())

                        } else {
                            // console.log(`currentGuessRowIndex: ${currentGuessRowIndex}, totalGuesses: ${totalGuesses}, body.step: ${body.step}`)
                            if (currentGuessRowIndex >= totalGuesses || body.step == 'LOSS') {
                                gameIsOver = true
                                showMessage('Game Over')
                                    .then(() => resetIfNeeded())
                            }
                            if (currentGuessRowIndex <= totalGuesses) {
                                currentGuessRowIndex++
                                currentGuessLetterIndex = 0
                            }
                        }
                    }

                })
            })
            .catch(error => showInternalErrorMessage(error))
    }
}

const handleClick = (clickedLetter) => {
    if (!gameIsOver) {
        if (clickedLetter === DELETE_KEY) {
            deleteLetter()
            return
        }
        if (clickedLetter === ENTER_KEY) {
            checkRow()
            return
        }
        addLetter(clickedLetter)
    }
}

const findGuessElementLetterByRowIndexAndLetterIndex = (rowIndex, letterIndex) => {
    return document.getElementById('guess-row-' + rowIndex + '-guess-letter-' + letterIndex)
}

const addLetter = (clickedLetter) => {
    if (currentGuessLetterIndex < wordSize && currentGuessRowIndex <= totalGuesses) {
        const guessLetter = findGuessElementLetterByRowIndexAndLetterIndex(currentGuessRowIndex, currentGuessLetterIndex)
        guessLetter.textContent = clickedLetter
        guessDataRows[currentGuessRowIndex][currentGuessLetterIndex] = clickedLetter
        guessLetter.setAttribute('typed-letter', clickedLetter)
        currentGuessLetterIndex++
    }
}

const deleteLetter = () => {
    if (currentGuessLetterIndex > 0) {
        currentGuessLetterIndex--
        const guessLetter = findGuessElementLetterByRowIndexAndLetterIndex(currentGuessRowIndex, currentGuessLetterIndex)
        guessLetter.textContent = ''
        guessDataRows[currentGuessRowIndex][currentGuessLetterIndex] = ''
        guessLetter.setAttribute('typed-letter', '')
    }
}

const showMessage = (message) => {
    const messageElement = document.createElement('p')
    messageElement.textContent = message
    messageDisplay.append(messageElement)
    return new Promise((resolve, reject) =>
        setTimeout(() => {
            messageDisplay.removeChild(messageElement)
            return resolve()
        }, DEFAULT_MESSAGE_TIME_DURATIONT)
    )
}

const addColorToKey = (keyLetter, color) => {
    const key = document.getElementById(keyLetter)
    key.classList.add(color)
}

const flipAllGuessLetters = (currentState) => {
    return currentState.forEach((guess, guessIndex) => {
        flipGuessLetters(guess.guessStateRowList, guess.id)
    })
}

const flipGuessLetters = (guessStateRowList, guessId) => {
    const guessRow = document.querySelector('#guess-row-' + guessId).childNodes
    const guessData = []
    guessRow.forEach(guessLetter => {
        guessData.push({letter: guessLetter.getAttribute('typed-letter'), color: 'grey-overlay'})
    })
    guessStateRowList.forEach((letterState, letterStateIndex) => {
        if ("CORRECT" == letterState.state) {
            guessData[letterStateIndex].color = 'green-overlay'
        } else if ("CONTAIN" == letterState.state) {
            guessData[letterStateIndex].color = 'yellow-overlay'
        }
    })
    guessRow.forEach((guessLetter, index) => {
        if (!guessLetter.classList.contains('flip')) {
            setTimeout(() => {
                guessLetter.classList.add('flip')
                guessLetter.classList.add(guessData[index].color)
                addColorToKey(guessData[index].letter, guessData[index].color)
            }, DEFAULT_ANIMATION_TIMEOUT * index)
        }
    })
}

resetIfNeeded()
