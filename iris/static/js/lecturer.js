const options = {valueNames: ['name']}
const courseList = new List('course-existing', options)
const searchField = document.getElementById('course-search')
const snackbar = document.getElementById('course_added_notif')

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

courseList.sort('name')

function applyFilter () {
  // Hides all items when the search field is empty
  courseList.filter(function (item) {
    return searchField.value !== ''
  })
}

applyFilter()
courseList.on('searchComplete', applyFilter)

/* eslint-disable*/
function addCourse (e) {
  // e.preventDefault()

  let course = e.text.replace(/\s/g, '').split('-')

  let courseCode = course[0]
  let courseName = course[1]
  let data = {
    message: courseCode + ' added.',
    timeout: 2000
  }

  if (courseCode && courseName) {
    console.log('Course assigned')
    socket.emit('lecturer_course_existing_send', {
      'code': courseCode,
      'name': courseName
    })
    searchField.value = ''
    snackbar.MaterialSnackbar.showSnackbar(data)
    applyFilter()
  }
  return false
}
/* eslint-enable*/

socket.on('lecturer_course_existing_recv', function (msg) {
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
