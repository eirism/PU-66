let socket = io()

$('#course-new').submit(function () {
  let courseCode = $('#course-new-code')
  let courseName = $('#course-new-name')
  if (courseCode.val() && courseName.val()) {
    console.log('Course submitted')
    socket.emit('lecturer_course_new_send', {
      'code': courseCode.val(),
      'name': courseName.val()
    })
    courseCode.val('')
    courseName.val('')
  }
  return false
})

socket.on('lecturer_course_new_recv', function (msg) {
  let code = msg['code']
  let name = msg['name']

  $('#table_courses').children().append(
    '<tr>' +
      '<td class="table_row mdl-data-table__cell--non-numeric">' +
        '<a class="course_links" href="/lecturer/' + code + '/session">' + code + ' - ' + name + '</a>' +
      '</td>' +
    '</tr>'
  )
})
