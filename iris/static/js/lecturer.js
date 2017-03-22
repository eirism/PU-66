let socket = io()

$('#course-new').submit(function () {
  let courseCode = $('#course-new-code')
  let courseName = $('#course-new-name')
  if (courseCode.val() && courseName.val()) {
    console.log('Course submitted')
    socket.emit('lecturer_course_new', {
      'code': courseCode.val(),
      'name': courseName.val()
    })
    courseCode.val('')
    courseName.val('')
  }
  return false
})
