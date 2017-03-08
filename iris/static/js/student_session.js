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

socket.on('student_recv', function (msg) {
  console.log(msg['active'])
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

$('form').submit(function(){
  let q_field = $('#questionInput')
  if(q_field.val()) {
    console.log('Message submitted')
    socket.emit('student_send', {'question': q_field.val(), 'course_id': courseID, 'action': 0})
    q_field.val('')
  }
  return false
})

socket.on('student_recv', function (msg) {
  console.log(msg)
  let receivedStatus = msg.hasOwnProperty('active')
  console.log(receivedStatus)
  if(!receivedStatus) {
    $('#questions').prepend('<li class="mdl-list__item-text-body"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-icon">person</i>' + msg['question'] + '</span></li>')
  }
})
