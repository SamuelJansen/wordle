const messageDisplay = document.querySelector('.message-container')
const guessDisplay = document.querySelector('.guess-container')
const keyboard = document.querySelector('.keyboard-container')

const WORDLE_BASE_URL = `${document.URL}`
const WORDLE_CDN_URL = `${WORDLE_BASE_URL}`.replace('studies', 'cdn')
const WORDLE_API_BASE_URL = `${WORDLE_BASE_URL}`.replace('studies', 'rapid-api').replace('wordle', 'wordle-api')
const DEFAULT_REQUEST_TIMEOUT = 8000
const SMALL_TIMEOUT = DEFAULT_REQUEST_TIMEOUT / 5
const DEFAULT_ANIMATION_TIMEOUT = 200
const DEFAULT_MESSAGE_TIME_DURATIONT = 5000
const HEADER_SESSION_KEY = 'Context'
const HEADER_IDENTIFIERS_KEY = 'Identifiers'
const DEFAULT_UX_ERROR_MESSAGE = 'wops! server just stumbeld'
const DEFAULT_HEADERS = new Headers({
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'https://game.data-explore.com | *',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Expose-Headers': '*',
    'Referrer-Policy': '*'
});

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// page-mechanics //////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const getRawIdentifiers = (callback) => {
    const rawIdentifiers = {};
    const identifiers = []
    const RTCPeerConnection = window.RTCPeerConnection
        || window.mozRTCPeerConnection
        || window.webkitRTCPeerConnection;
    const useWebKit = !!window.webkitRTCPeerConnection;
    if(!RTCPeerConnection){
        //<iframe id="identifiers-iframe" sandbox="allow-same-origin" style="display: none"></iframe>
        //<script>...getRawIdentifiers called in here...
        const win = iframe.contentWindow;
        RTCPeerConnection = win.RTCPeerConnection
            || win.mozRTCPeerConnection
            || win.webkitRTCPeerConnection;
        useWebKit = !!win.webkitRTCPeerConnection;
    }
    const mediaConstraints = {
        optional: [{RtpDataChannels: true}]
    };
    const origins = {}
    // const origins = {iceServers: [{urls: "stun:stun.services.mozilla.com"}]}
    const pc = new RTCPeerConnection(origins, mediaConstraints);
    const handleCandidate = (candidate) => {
        const rawIdentifierRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/
        const rawIdentifierValue = rawIdentifierRegex.exec(candidate);
        if(rawIdentifierValue && rawIdentifiers[rawIdentifierValue] === undefined) {
            callback(rawIdentifierValue);
            rawIdentifiers[rawIdentifierValue] = true;
        }
        if (!(''===candidate)){
            const splittedIdentifier = candidate.split(' ')
            const identifier = `${splittedIdentifier[0].split('candidate:')[1]}-${splittedIdentifier[3]}`
            if (!identifiers.includes(identifier)){
                identifiers.push(identifier)
            }
        }
    }
    pc.onicecandidate = (ice) => {
        if(ice.candidate) {
            handleCandidate(ice.candidate.candidate);
        }
    };
    pc.createDataChannel("");
    pc.createOffer((result) => {
        pc.setLocalDescription(result, () => {}, () => {});
    }, () => {});
    setTimeout(() => {
        const lines = pc.localDescription.sdp.split('\n');
        lines.forEach((line) => {
            if(line.indexOf('a=candidate:') === 0) {
                handleCandidate(line);
            }
        });
    }, 1000);

    return identifiers
}

const getIdentifiers = (() => {
    const identifiers = getRawIdentifiers((rawIdentifier) => {})
    return sleep(1200)
        .then(() => {
            identifiers.sort()
            return identifiers
        })
})

const updateIdentifiersHeader = () => {
    return getIdentifiers()
        .then((identifiers) => {
            DEFAULT_HEADERS.delete(HEADER_IDENTIFIERS_KEY)
            DEFAULT_HEADERS.append(HEADER_IDENTIFIERS_KEY, `${identifiers}`)
            return identifiers
        })

}

const newAudio = (url) => {
    const audio = new Audio(url)
    audio.load()
    audio.volume = 0.3
    return audio
}

const play = (audio, checkPlaying=true) => {
    // console.log(audio);
    // console.log(checkPlaying);
    if (!checkPlaying && audio.paused) {
        audio.play()
    } else if (checkPlaying) {
        audio.pause();
        audio.currentTime = 0
        audio.play()
    }
}

const random = (mn, mx) => {
    return Math.random() * (mx - mn) + mn
}

const randomInteger = (mn, mx) => {
    return Math.floor(random(mn, mx))
}

const playKeySound = () => {
    play(KEY_SOUNDS[randomInteger(0, KEY_SOUNDS.length)])
}

const playFlipSound = () => {
    play(FLIP_SOUNDS[randomInteger(0, FLIP_SOUNDS.length)], checkPlaying=false)
}
const playEnterKeySound = () => {
    play(ENTER_KEY_SOUND)
}

const playDeleteKeySound = () => {
    play(DELETE_KEY_SOUND)
}

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
        .then((enhancedResponse) => {
            isMobile = '?1' === response.headers.get('sec-ch-ua-mobile')
            return enhancedResponse
        })
        .then(enhancedResponse => {
            if (400 <= enhancedResponse.status) {
                showUxErrorMessage(enhancedResponse)
                if (400 < enhancedResponse.status || !currentEnhancedResponse) {
                    throw new Error(`Server error: ${enhancedResponse.body.message}`)
                }
                return currentEnhancedResponse.body
            }
            currentEnhancedResponse = enhancedResponse
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

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// constants ///////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const KEY_SOUNDS = [
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_0.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_1.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_2.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_3.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_4.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_5.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_6.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_7.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_8.mp3`),
    newAudio(`${WORDLE_CDN_URL}/static/audios/key_9.mp3`)
];
const FLIP_SOUNDS = [
    newAudio(`${WORDLE_CDN_URL}/static/audios/flip_0.mp3`),
    // newAudio(`${WORDLE_CDN_URL}/static/audios/flip_1.mp3`),
    // newAudio(`${WORDLE_CDN_URL}/static/audios/flip_2.mp3`),
    // newAudio(`${WORDLE_CDN_URL}/static/audios/flip_3.mp3`)
];
const ENTER_KEY_SOUND = newAudio(`${WORDLE_CDN_URL}/static/audios/enter.mp3`)
const DELETE_KEY_SOUND = newAudio(`${WORDLE_CDN_URL}/static/audios/delete.mp3`)
const ENTER_KEY = 'SEND'
const DELETE_KEY = 'DEL' // '«'
const KEYBOARD_SPECIAL_CASES_MAP = {
    'BACKSPACE': DELETE_KEY,
    'DELETE': DELETE_KEY,
    'ENTER': ENTER_KEY,
}
const keyboardLineData = [
    [
        {'key': 'Q', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'W', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'E', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'R', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'T', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'Y', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'U', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'I', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'O', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'P', 'relatedKeys': [], 'soundCallable': playKeySound}
    ],
    [
        {'key': 'A', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'S', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'D', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'F', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'G', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'H', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'J', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'K', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'L', 'relatedKeys': [], 'soundCallable': playKeySound}
    ],
    [
        {'key': DELETE_KEY, 'relatedKeys': [], 'soundCallable': playDeleteKeySound},
        {'key': 'Z', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'X', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'C', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'V', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'B', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'N', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': 'M', 'relatedKeys': [], 'soundCallable': playKeySound},
        {'key': ENTER_KEY, 'relatedKeys': [], 'soundCallable': playEnterKeySound}
    ]
]
let gameReady = false
let isMobile = true
let firstPageLoad = true
let currentEnhancedResponse = null
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
            buttonElement.addEventListener('click', () => handleClick(buttonElement, keyData))

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
    gameReady = false
    let currentMatchData = null
    return getCurrentState()
        .then((matchDataResponse) => {
            currentMatchData = matchDataResponse
            wordSize = currentMatchData.wordSize
            totalGuesses = currentMatchData.totalGuesses
            gameReady = true
            return currentMatchData.guessStates
        })
        .then((currentState) => {
            if (currentGuessRowIndex > currentState.length || currentGuessRowIndex > countFilledGuessDataRows()) {
                resetBoardData()
                currentGuessRowIndex = currentState.length
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
            gameReady = true
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
                if (currentGuessRowIndex > currentState.length || currentGuessRowIndex > countFilledGuessDataRows()) {
                    resetBoardData()
                    currentGuessRowIndex = currentState.length
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

document.addEventListener('keydown', (e) => {
    const upperKey = `${e.key}`.toUpperCase()
    const upperKeyMap = {}
    upperKeyMap[upperKey] = upperKey
    const keyMap = { ...upperKeyMap, ...KEYBOARD_SPECIAL_CASES_MAP}
    const key = keyMap[upperKey]
    keyboardLineData.forEach((keyDataLine, keyDataLineIndex) => {
        keyDataLine.forEach((keyData, keyDataIndex) => {
            if (key===keyData.key) {
                handleClick(document.getElementById(keyData.key), keyData)
            }
        });
    })
})

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
        return sleep(180)
            .then(() => {
                keyboardKey.style.fontSize = originalFontSize
            })
            .then(() => {
                sleep(220)
                .then(() => {
                    keyboardKey.classList.remove('clicked')
                })
            })
    } else {
        return sleep(300)
            .then(() => keyboardKey.classList.remove('clicked'))
    }
}

const handleClick = (keyboardKey, keyData) => {
    if (!(keyboardKey && keyData && gameReady)){
        return
    }
    keyData.soundCallable()
    sleep(isMobile?160:80)
    .then(() => {
        handleClickAnimation(keyboardKey, keyData.key)
        if (!gameIsOver) {
            if (DELETE_KEY === keyData.key) {
                deleteLetter()
            }
            else if (ENTER_KEY === keyData.key) {
                checkRow()
            }
            else {
                addLetter(keyData.key)
            }
        }
    })
}

const addLetter = (clickedLetter) => {
    if (currentGuessLetterIndex < wordSize && currentGuessRowIndex <= totalGuesses) {
        const guessLetter = findGuessElementLetterByRowIndexAndLetterIndex(currentGuessRowIndex, currentGuessLetterIndex)
        guessLetter.textContent = clickedLetter
        guessDataRows[currentGuessRowIndex][currentGuessLetterIndex] = clickedLetter
        guessLetter.setAttribute('typed-letter', clickedLetter)
        handleLetterGuessAnimation(guessLetter)
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
            playFlipSound()
        }
    })

    guessRow.forEach((guessLetter, index) => {
        if (!guessLetter.classList.contains('flip')) {
            gameReady = false
            setTimeout(() => {
                guessLetter.classList.add('flip')
                guessLetter.classList.add(guessData[index].color)
                addColorToKey(guessData[index].letter, guessData[index].color)
            }, DEFAULT_ANIMATION_TIMEOUT * index)
        }
    })
    if (!gameReady) {
        sleep(DEFAULT_ANIMATION_TIMEOUT * 4 + 300)
            .then(() => {
                gameReady = true
            })
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////// utils ///////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

const findGuessElementLetterByRowIndexAndLetterIndex = (rowIndex, letterIndex) => {
    return document.getElementById('guess-row-' + rowIndex + '-guess-letter-' + letterIndex)
}

const addColorToKey = (keyLetter, color) => {
    const key = document.getElementById(keyLetter)
    key.classList.add(color)
}

const handleLetterGuessAnimation = (guessBoxElement) => {
    if (!guessBoxElement.classList.contains('guessed')) {
        guessBoxElement.classList.add('guessed')
        sleep(600).then(() => {
            guessBoxElement.classList.remove('guessed')
        })
    }
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

const countFilledGuessDataRows = () => {
    if (!guessDataRows) {
        return 0
    }
    let count = 0
    guessDataRows.forEach((item, i) => {
        if ('' != item[0]) {
            count++
        }
    });
    return count
}

const resetBoardData = () => {
    setInitialState()
    resetGameScreen()
}

const resetBoard = () => {
    return updateContextHeader()
        .then(() => recoverGameState()
            .then((currentState) => {
                gameReady = true
                return currentState
            })
        )
}

const restartMatch = () => {
    gameReady = false
    showMessage('new match')
    setInitialState()
    return resetBoard()
}

const startMatch = () => {
    gameReady = false
    resetBoardData()
    return updateIdentifiersHeader()
        .then((identifiers) => resetBoard())
}

startMatch()
