const buttonSlow = document.getElementById('slow')
const buttonFast = document.getElementById('fast')
const buttonEasy = document.getElementById('easy')
const buttonHard = document.getElementById('hard')
const questionButton = document.getElementById('questionButton')
const timeOut = 15000
let paceClicked = false
let difficultyClicked = false
let paceTimeOut
let difficultyTimeOut
let currentTime
let timePace
let timeDifficulty
let socket = io()
socket.emit('join', {'course_id': courseID})

function enableAllButtons () {
  buttonSlow.disabled = false
  buttonFast.disabled = false
  buttonEasy.disabled = false
  buttonHard.disabled = false
  questionButton.disabled = false
}

function disableAllButtons () {
  buttonSlow.disabled = true
  buttonFast.disabled = true
  buttonEasy.disabled = true
  buttonHard.disabled = true
  questionButton.disabled = true
}

if (!sessionActive) {
  disableAllButtons()
}

function setTimers () {
  currentTime = new Date()
  if (localStorage.getItem('timePace')) {
    let timePace = new Date(localStorage.getItem('timePace'))
    let timeRemainingPace = timeOut - (currentTime.getTime() - timePace.getTime())
    if (timeRemainingPace > 0) {
      buttonSlow.disabled = true
      buttonFast.disabled = true
    }
    paceTimeOut = setTimeout(function () {
      if (sessionActive) {
        buttonSlow.disabled = false
        buttonFast.disabled = false
        paceClicked = false
      }
    }, timeRemainingPace)
  }
  if (localStorage.getItem('timeDifficulty')) {
    let timeDifficulty = new Date(localStorage.getItem('timeDifficulty'))
    let timeRemainingDifficulty = timeOut - (currentTime.getTime() - timeDifficulty.getTime())
    if (timeRemainingDifficulty > 0) {
      buttonEasy.disabled = true
      buttonHard.disabled = true
    }
    difficultyTimeOut = setTimeout(function () {
      if (sessionActive) {
        buttonEasy.disabled = false
        buttonHard.disabled = false
        difficultyClicked = false
      }
    }, timeRemainingDifficulty)
  }
}

function timeOutPace () {
  buttonSlow.disabled = true
  buttonFast.disabled = true
  paceClicked = true
  timePace = new Date()
  localStorage.setItem('timePace', timePace)
  paceTimeOut = setTimeout(function () {
    if (sessionActive) {
      buttonSlow.disabled = false
      buttonFast.disabled = false
      paceClicked = false
    }
  }, timeOut)
}
buttonSlow.addEventListener('click', timeOutPace)
buttonFast.addEventListener('click', timeOutPace)

function timeOutDifficulty () {
  buttonEasy.disabled = true
  buttonHard.disabled = true
  difficultyClicked = true
  timeDifficulty = new Date()
  localStorage.setItem('timeDifficulty', timeDifficulty)
  difficultyTimeOut = setTimeout(function () {
    if (sessionActive) {
      buttonEasy.disabled = false
      buttonHard.disabled = false
      difficultyClicked = false
    }
  }, timeOut)
}
buttonEasy.addEventListener('click', timeOutDifficulty)
buttonHard.addEventListener('click', timeOutDifficulty)

window.onbeforeunload = function () {
  if (paceClicked && (buttonSlow.disabled || buttonFast.disabled)) {
    localStorage.setItem('timePace', timePace)
    clearTimeout(paceTimeOut)
  }
  if (difficultyClicked && (buttonHard.disabled || buttonEasy.disabled)) {
    localStorage.setItem('timeDifficulty', timeDifficulty)
    clearTimeout(difficultyTimeOut)
  }
}

window.onload = function () {
  setTimers()
}

$('.action_button').click(function (eventObj) {
  console.log(eventObj['currentTarget']['id'])
  let data = {'action': eventObj['currentTarget']['id'], 'course_id': courseID}
  socket.emit('student_send', data)
})

$('form').submit(function () {
  let qField = $('#questionInput')
  if (qField.val()) {
    console.log('Message submitted')
    socket.emit('student_send', {'question': qField.val(), 'course_id': courseID})
    qField.val('')
  }
  return false
})

socket.on('student_recv', function (msg) {
  console.log(msg)
  let receivedStatus = msg.hasOwnProperty('active')
  console.log(receivedStatus)
  let questionLog = $('.questions-log')
  if (msg.hasOwnProperty('question')) {
    if (questionLog.has('p').length) {
      questionLog.empty()
    }
    let question = msg['question'][0]
    let groupNum = msg['question'][1]
    let response = msg['question'][2]
    let questionList = $('#questions-' + groupNum)
    if (!questionList.length) {
      questionList = $('<ul>', {id: 'questions-' + groupNum, 'class': 'mdl-list'})
      if (!questionLog.is(':empty')) {
        questionLog.prepend('<hr>')
      }
      questionLog.prepend(questionList)
    }
    if (response === null) {
      questionList.prepend('<li class="mdl-list__item"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-icon">person</i>' + question + '</span></li>')
    } else {
      questionList.prepend('<li class="mdl-list__item"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-icon">person</i>' + question + '</span></li>' + '&emsp; <i>Response: </i>' + response)
    }
  }
  if (msg.hasOwnProperty('command')) {
    if (msg['command'] === 'deleteQuestions') {
      questionLog.empty().append('<p>No questions have been asked yet.</p>')
    }
  }
  if (msg.hasOwnProperty('active')) {
    sessionActive = msg['active']
    if (sessionActive) {
      enableAllButtons()
      setTimers()
    } else {
      disableAllButtons()
    }
  }
})

// Disable questionInput newline on enter, unless shift+enter is used
$('textarea').keydown(function (e) {
  if (e.keyCode === 13 && !e.shiftKey) {
    e.preventDefault()
    questionButton.click()
  }
})

// New response exists and questions should be updated to display possible responses
socket.on('new_response', function (msg) {
  console.log('new response received')
  if (msg.hasOwnProperty('reload')) {
    if (msg['reload']) {
      window.location.reload(true)
    }
  }
})
