const buttonStart = document.getElementById('button_start')
const buttonStop = document.getElementById('button_stop')
const buttonResponse = document.getElementById('add_response')
let socket = io()
let modal
socket.emit('join', {'course_id': courseID})

function disableStart () {
  buttonStart.disabled = true
  buttonStop.disabled = false
}

function disableStop () {
  buttonStart.disabled = false
  buttonStop.disabled = true
}

if (sessionActive) {
  disableStart()
} else {
  disableStop()
}

buttonStart.onclick = function () {
  disableStart()

  console.log('SESSION START')
  let data = {'session_control': 'start', 'course_id': courseID}
  socket.emit('lecturer_send', data)
}

buttonStop.onclick = function () {
  disableStop()

  console.log('SESSION STOP')
  let data = {'session_control': 'stop', 'course_id': courseID}
  socket.emit('lecturer_send', data)
}

buttonResponse.onclick = function () {
  console.log('Entering response scope')
  let kField = $('#keywords')
  let rField = $('#response')
  if(kField.val() && rField.val() ) {
    console.log('Sending keyword/response')
    let data = {'keywords': kField.val(), 'response': rField.val(), 'course_id': courseID}
    console.log(data)
    socket.emit('lecturer_keyword_new', data);
    kField.val('')
    rField.val('')
  }
  return false
}

let actions = ['slow', 'fast', 'easy', 'hard']

socket.on('lecturer_recv', function (msg) {
  let questionLog = $('.questions-log')
  if (msg.hasOwnProperty('action')) {
    console.log(msg['action'])
    $('#text_' + msg['action'][0]).attr('data-badge', msg['action'][1])
    if ($.inArray(msg['action'][0], actions.slice(0, 2)) !== -1) {
      speed.data.datasets[0].data[actions.indexOf(msg['action'][0])] = parseInt($('#text_' + msg['action'][0]).attr('data-badge'))
      speed.update()
    } else {
      difficulty.data.datasets[0].data[actions.indexOf(msg['action'][0]) - 2] = parseInt($('#text_' + msg['action'][0]).attr('data-badge'))
      difficulty.update()
    }
  } else if (msg.hasOwnProperty('question')) {
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
      questionList.prepend('<li class="mdl-list__item"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-icon">person</i>' + question + '</span></li>' + '&emsp; <i>Response: </i>' +  response)
    }
  } else if (msg.hasOwnProperty('active')) {
    console.log(msg['active'])
    if (msg['active']) {
      disableStart()
    } else {
      disableStop()
    }
  } else if (msg.hasOwnProperty('command')) {
    if (msg['command'] === 'deleteQuestions') {
      questionLog.empty().append('<p>No questions have been asked yet.</p>')
    }
  }
})

let ctxSpeed = $('#speed')

let speed = new Chart(ctxSpeed, {
  type: 'doughnut',
  data: {
    datasets: [{
      data: [
        parseInt($('#text_slow').attr('data-badge')),
        parseInt($('#text_fast').attr('data-badge'))
      ],
      backgroundColor: [
        'rgba(172, 236, 0, 0.75)',
        'rgba(0, 187, 214, 0.75)'
      ]
    }],
    labels: [
      'Slow',
      'Fast'
    ]
  },
  options: {
    responsive: false
  }
})

let ctxDifficulty = $('#difficulty')

let difficulty = new Chart(ctxDifficulty, {
  type: 'doughnut',
  data: {
    datasets: [{
      data: [
        parseInt($('#text_easy').attr('data-badge')),
        parseInt($('#text_hard').attr('data-badge'))
      ],
      backgroundColor: [
        'rgba(186, 101, 201, 0.75)',
        'rgba(239, 60, 121, 0.75)'
      ]
    }],
    labels: [
      'Easy',
      'Hard'
    ]
  },
  options: {
    responsive: false
  }
})

let dialog = document.querySelector('dialog')
let showDialogButton = document.querySelector('#show-dialog')
if (!dialog.showModal) {
    dialogPolyfill.registerDialog(dialog)
}
showDialogButton.addEventListener('click', function () {
    dialog.showModal()
    modal = true
})
dialog.querySelector('.close').addEventListener('click', function () {
    dialog.close()
    modal = false
})

socket.on('new_response', function (msg) {
  console.log('new response received')
  localStorage.setItem('modal_open', modal)
  if(msg.hasOwnProperty('reload')) {
    if(msg['reload']) {
      window.location.reload(true)
    }
  }
})

//Disables newline on enter, allows shift-enter
$('form').keydown(function (e) {
  if (e.keyCode === 13 && !e.shiftKey) {
    e.preventDefault()
    buttonResponse.click()
  }
})
