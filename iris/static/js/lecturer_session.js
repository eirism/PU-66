const buttonStart = document.getElementById('button_start')
const buttonStop = document.getElementById('button_stop')
const cardTitle = document.getElementById('card_title')
let socket = io()
socket.emit('join', {'course_id': courseID})

function disableStart () {
  buttonStart.disabled = true
  buttonStop.disabled = false
  cardTitle.innerHTML = 'Session active'
  $('.mdl-card__title').css('background-color', '#E91E63')
}

function disableStop () {
  buttonStart.disabled = false
  buttonStop.disabled = true
  cardTitle.innerHTML = 'Session not active'
  $('.mdl-card__title').css('background-color', '#2196F3')
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

let actions = ['slow', 'fast', 'easy', 'hard']

socket.on('lecturer_recv', function (msg) {
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
    $('#questions').prepend('<li class="mdl-list__item-text-body"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-icon">person</i>' + msg['question'] + '</span></li>')
  } else if (msg.hasOwnProperty('active')) {
    console.log(msg['active'])
    if (msg['active']) {
      disableStart()
    } else {
      disableStop()
    }
  } else if (msg.hasOwnProperty('command')) {
    if (msg['command'] === 'deleteQuestions') {
      $('ul').empty()
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
  }
})
