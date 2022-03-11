const messageDisplay = document.querySelector('.message-container')
const guessDisplay = document.querySelector('.guess-container')
const keyboard = document.querySelector('.keyboard-container')

const WORDLE_API_BASE_URL = `${document.URL}/api`
const DEFAULT_REQUEST_TIMEOUT = 5000
const SMALL_TIMEOUT = DEFAULT_REQUEST_TIMEOUT / 5
const DEFAULT_ANIMATION_TIMEOUT = 200
const DEFAULT_MESSAGE_TIME_DURATIONT = 5000
const HEADER_SESSION_KEY = 'Context'
const DEFAULT_UX_ERROR_MESSAGE = 'wops! server just stumbeld'
const DEFAULT_HEADERS = new Headers({
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
});

const ENTER_KEY = 'SEND'
const DELETE_KEY = 'DEL' // '«'
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
        {'key': DELETE_KEY, 'relatedKeys': []},
        {'key': 'Z', 'relatedKeys': []},
        {'key': 'X', 'relatedKeys': []},
        {'key': 'C', 'relatedKeys': []},
        {'key': 'V', 'relatedKeys': []},
        {'key': 'B', 'relatedKeys': []},
        {'key': 'N', 'relatedKeys': []},
        {'key': 'M', 'relatedKeys': []},
        {'key': ENTER_KEY, 'relatedKeys': []}
    ]
]
let firstPageLoad = true
let guessDataRows = null
let wordSize = null
let totalGuesses = null
let currentGuessRowIndex = null
let currentGuessLetterIndex = null
let gameIsOver = null

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// screen-flow /////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const addGuessesScreen = () => {
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
}

const removeGuessesScreen = () => {
    return guessDataRows.forEach((guessRowContent, guessRowIndex) => {
        oldGuessRow = document.querySelector('#guess-row-' + guessRowIndex)
        if (oldGuessRow) {
            oldGuessRow.remove()
        }
    })
}

const resetGuessesScreen = () => {
    removeGuessesScreen()
    addGuessesScreen()
}

const addKeyboardScreen = () => {
    return keyboardLineData.forEach((keyDataLine, keyDataLineIndex) => {
        const keyboardLine = document.createElement('div')
        keyboardLine.classList.add('keyboard-line-container')
        keyDataLine.forEach((keyData, keyDataIndex) => {
            const buttonElement = document.createElement('button')
            buttonElement.textContent = keyData.key
            buttonElement.setAttribute('id', keyData.key)
            buttonElement.setAttribute('class', 'keyboard-key')
            buttonElement.addEventListener('click', () => handleClick(buttonElement, keyData.key))
            keyboardLine.append(buttonElement)
        });
        keyboard.append(keyboardLine)
    })
}

const removeKeyboardScreen = () => {
    return keyboardLineData.forEach((item, i) => {
        oldKeyboardLine = document.querySelector('.keyboard-line-container')
        if (oldKeyboardLine) {
            oldKeyboardLine.remove()
        }
    });
}

const resetKeyboardScreen = () => {
    removeKeyboardScreen()
    addKeyboardScreen()
}

const buildGameScreen = () => {
    addGuessesScreen()
    addKeyboardScreen()
}

const removeGameScreen = () => {
    removeGuessesScreen()
    removeKeyboardScreen()
}

const resetGameScreen = () => {
    resetGuessesScreen()
    resetKeyboardScreen()
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// game-state //////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const updateContextHeader = () => {
    return fetchWithTimeout(`${WORDLE_API_BASE_URL}/match/authenticate`,
        {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            handler: updateContextHeader
        }
    )
        .then(response => getResponseBody(response))
        .then(contextResponse => {
            DEFAULT_HEADERS.delete(HEADER_SESSION_KEY)
            DEFAULT_HEADERS.append(HEADER_SESSION_KEY, `Bearer ${contextResponse.context}`)
            return contextResponse
        })
        .catch(error => showInternalErrorMessage(error))
}

const handleUnauthorisedSession = (response) => {
    if (401 === response.status) {
        console.log('Unauthorized session. Restarting match')
        restartMatch()
        throw Error('Match restarted')
    }
}

const getCurrentState = () => {
    return fetchWithTimeout(`${WORDLE_API_BASE_URL}/match`,
        {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            handler: getCurrentState
        }
    )
        .then(response => getResponseBody(response))
        .then((matchData) => {
            if (firstPageLoad && 0 < matchData.guessStates.length) {
                showMessage('welcomeback')
            }
            firstPageLoad = false
            return matchData
        })
        .catch(error => {
            showInternalErrorMessage(error)
            throw Error('Not possible to get matchData')
        })
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// game-logic //////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const recoverGameState = () => {
    let currentMatchData = null
    return getCurrentState()
        .then((matchDataResponse) => {
            currentMatchData = matchDataResponse
            wordSize = currentMatchData.wordSize
            totalGuesses = currentMatchData.totalGuesses
            return currentMatchData.guessStates
        })
        .then((currentState) => {
            if (0 < currentState.length && currentGuessRowIndex >= currentState.length) {
                recoverGameState()
                throw new Error('Delayed response...')
            }
            resetBoardData()
            currentGuessRowIndex = currentState.length
            currentState.forEach((guess, guessIndex) => {
                guess.guessStateRowList.forEach((guessLetter, guessLetterIndex) => {
                    guessDataRows[guess.id][guessLetter.id] = guessLetter.key
                    guessElementLetter = findGuessElementLetterByRowIndexAndLetterIndex(guess.id, guessLetter.id)
                    guessElementLetter.textContent = guessLetter.key
                    guessElementLetter.setAttribute('typed-letter', guessLetter.key)
                });
            });
            flipAllGuessLetters(currentState)
            return currentState
        })
}

const checkRow = () => {
    const wordGuess = guessDataRows[currentGuessRowIndex].join('')
    let currentMatchData = null
    if (currentGuessLetterIndex >= wordSize) {
        return fetchWithTimeout(`${WORDLE_API_BASE_URL}/match/verify?word=${wordGuess}`, {
            method: 'PATCH',
            headers: DEFAULT_HEADERS
        })
            .then((response) => getResponseBody(response))
            .then((matchDataResponse) => {
                currentMatchData = matchDataResponse
                return currentMatchData.guessStates
            })
            .then((currentState) => {
                if (currentGuessRowIndex > currentState.length) {
                    recoverGameState()
                    throw new Error('Delayed response...')
                }
                currentState.forEach((guess, guessIndex) => {
                    if (currentGuessRowIndex === guess.id) {
                        flipGuessLetters(guess.guessStateRowList, guess.id)
                        if ('VICTORY' === currentMatchData.step) {
                            gameIsOver = true
                            showMessage('perfect!')
                                .then(() => restartMatch())
                        } else {
                            if (currentGuessRowIndex >= totalGuesses || 'LOSS' === currentMatchData.step) {
                                gameIsOver = true
                                showMessage(`aawww... the word was "${currentMatchData.correctWord}"`)
                                    .then(() => restartMatch())
                            }
                            if (currentGuessRowIndex <= totalGuesses) {
                                currentGuessRowIndex++
                                currentGuessLetterIndex = 0
                            }
                        }
                    }

                })
            })
            .catch(error => {
                showInternalErrorMessage(error)
                recoverGameState()
            })
    }
    else {
        showMessage('complete the word', timeout=2000)
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// helpers /////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const showUxErrorMessage = (enhancedResponse) => {
    if (500 > enhancedResponse.status) {
        return showMessage(enhancedResponse.body.message)
    }
    showMessage(DEFAULT_UX_ERROR_MESSAGE)
    resetBoard()
}

const showInternalErrorMessage = (error) => {
    console.log(error)
    if (!error.message) {
        console.log(`No message present. "error.message: ${error.message}"`)
    }
}

const showMessage = (message, options={}) => {
    if (message) {
        const { timeout = DEFAULT_MESSAGE_TIME_DURATIONT } = options
        const messageElement = document.createElement('p')
        messageElement.textContent = message.toLowerCase()
        messageDisplay.append(messageElement)
        return new Promise((resolve, reject) =>
            setTimeout(() => {
                messageDisplay.removeChild(messageElement)
                return resolve()
            }, timeout)
        )
    }
}

const handleClickAnimation = (keyboardKey, clickedLetter) => {
    keyboardKey.classList.add('clicked')
    if (ENTER_KEY === clickedLetter || DELETE_KEY === clickedLetter) {
        if (ENTER_KEY === clickedLetter) {
            keyboardKey.disabled = true
            sleep(1500)
                .then(() => {
                    keyboardKey.disabled = false
                })
        }
        let originalFontSize = keyboardKey.style.fontSize
        keyboardKey.style.fontSize = '8px'
        return sleep(80)
            .then(() => {
                keyboardKey.style.fontSize = originalFontSize
            })
            sleep(220)
            .then(() => {
                keyboardKey.classList.remove('clicked')
            })
    } else {
        return sleep(300)
            .then(() => keyboardKey.classList.remove('clicked'))
    }
}

const handleClick = (keyboardKey, clickedLetter) => {
    handleClickAnimation(keyboardKey, clickedLetter)
    if (!gameIsOver) {
        if (DELETE_KEY === clickedLetter) {
            deleteLetter()
        }
        else if (ENTER_KEY === clickedLetter) {
            checkRow()
        }
        else {
            addLetter(clickedLetter)
        }
    }
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

var forceRedraw = function(element){
    if (!element) { return; }
    const n = document.createTextNode(' ');
    const disp = element.style.display;
    element.appendChild(n);
    element.style.display = 'none';
    console.log("here");
    setTimeout(() => {
        element.style.display = disp;
        n.parentNode.removeChild(n);
    }, 10);
}

const flipAllGuessLetters = (currentState) => {
    currentState.forEach((guess, guessIndex) => {
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
        if ("CORRECT" === letterState.state) {
            guessData[letterStateIndex].color = 'green-overlay'
        } else if ("CONTAIN" === letterState.state) {
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

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// utils ///////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

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

const sleep = (ms) => {
    return new Promise((resolve, reject) => setTimeout(resolve, ms));
}

const getResponseBody = (response) => {
    handleUnauthorisedSession(response)
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
                throw new Error(`Server error: ${enhancedResponse.body.message}`)
            }
            return enhancedResponse.body
        })
}

const fetchWithTimeout = (url, options={}) => {
    const { timeout = DEFAULT_REQUEST_TIMEOUT } = options
    const { handler = null } = options
    return Promise.race([
        fetch(url, options),
        new Promise((resolve, reject) =>
            setTimeout(() => reject(new Error('Request timeout')), timeout)
        )
    ])
        .catch(error => {
            if (!handler) {
                throw error
            }
            handler()
        })
}

const findGuessElementLetterByRowIndexAndLetterIndex = (rowIndex, letterIndex) => {
    return document.getElementById('guess-row-' + rowIndex + '-guess-letter-' + letterIndex)
}

const addColorToKey = (keyLetter, color) => {
    const key = document.getElementById(keyLetter)
    key.classList.add(color)
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// main ////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const setInitialState = () => {
    guessDataRows = [
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', '']
    ]
    wordSize = 5
    totalGuesses = 5
    currentGuessRowIndex = 0
    currentGuessLetterIndex = 0
    gameIsOver = false
}

const resetBoardDataAndRecoverGameState = () => {
    // resetBoardData()
    return recoverGameState()
}

const resetBoardData = () => {
    setInitialState()
    resetGameScreen()
}

const resetBoard = () => {
    // resetBoardData()
    return updateContextHeader()
        .then(() => recoverGameState())
}

const restartMatch = () => {
    showMessage('new match')
    return resetBoard()
}

const startMatch = () => {
    return resetBoard()
}

startMatch()
