const options = {valueNames: ['name']}
const courseList = new List('courses', options)
const searchField = document.getElementById('course-search')
courseList.sort('name')

function applyFilter () {
  // Hides all items when the search field is empty
  courseList.filter(function (item) {
    return searchField.value !== ''
  })
}

applyFilter()
courseList.on('searchComplete', applyFilter)
