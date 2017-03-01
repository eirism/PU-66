const buttonStart = document.getElementById('button_start')
const buttonStop = document.getElementById('button_stop')
const feedbackmsg = document.getElementById('lecturer_message')
let socket = io()
socket.emit('join', {'course_id': courseID})

function disableStart () {
  buttonStart.disabled = true
  buttonStop.disabled = false
  feedbackmsg.innerHTML = 'Session active'
}

function disableStop () {
  buttonStart.disabled = false
  buttonStop.disabled = true
  feedbackmsg.innerHTML = 'Session not active'
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

    // Updating the correct data field on the chart
    polar.data.datasets[0].data[actions.indexOf(msg['action'][0])] = parseInt($('#text_' + msg['action'][0]).attr('data-badge'))

    polar.update()
  } else if (msg.hasOwnProperty('active')) {
    console.log(msg['active'])
    if (msg['active']) {
      disableStart()
    } else {
      disableStop()
    }
  }
})

let ctx = $('#polar')

let polar = new Chart(ctx, {
  type: 'polarArea',
  data: {
    datasets: [{
      data: [
        parseInt($('#text_slow').attr('data-badge')),
        parseInt($('#text_fast').attr('data-badge')),
        parseInt($('#text_easy').attr('data-badge')),
        parseInt($('#text_hard').attr('data-badge'))
      ],
      backgroundColor: [
        'rgba(172, 236, 0, 0.75)',
        'rgba(0, 187, 214, 0.75)',
        'rgba(186, 101, 201, 0.75)',
        'rgba(239, 60, 121, 0.75)'
      ],
      label: 'My dataset' // for legend
    }],
    labels: [
      'Slow',
      'Fast',
      'Easy',
      'Hard'
    ]
  },
  options: {
    elements: {
      arc: {
        borderColor: 'rgba(0, 0, 0, 0.1)'
      }
    },
    startAngle: -0.25 * Math.PI
  }
})
