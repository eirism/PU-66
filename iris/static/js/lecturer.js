$(document).ready(function ($) {
  $('.table-row').click(function () {
    window.location = $(this).data('href')
  })
})
