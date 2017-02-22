/**
 * Created by s on 22.02.17.
 */

const timeOut = 15000;

function timeOutSlow(){
    document.getElementById("slow").disabled = true;
    setTimeout(function() {
        document.getElementById("slow").disabled = false;
    }, timeOut);
}
document.getElementById("slow").addEventListener("click", timeOutSlow);

function timeOutFast(){
    document.getElementById("fast").disabled = true;
    setTimeout(function() {
        document.getElementById("fast").disabled = false;
    }, timeOut);
}
document.getElementById("fast").addEventListener("click", timeOutFast);

function timeOutEasy(){
    document.getElementById("easy").disabled = true;
    setTimeout(function() {
        document.getElementById("easy").disabled = false;
    }, timeOut);
}
document.getElementById("easy").addEventListener("click", timeOutEasy);

function timeOutHard(){
    document.getElementById("hard").disabled = true;
    setTimeout(function() {
        document.getElementById("hard").disabled = false;
    }, timeOut);
}
document.getElementById("hard").addEventListener("click", timeOutHard);

var socket = io();
socket.emit('join', {'course_id': course_id });

$('form').submit(function(){
    var m_field = $('#m');
    var data = {'action': m_field.val()};
    console.log('Submitted: ' + data);
    socket.emit('student_send', data);
    m_field.val('');
    return false;
});

$('.action_button').click(function (eventObj) {
    console.log(eventObj['currentTarget']['id']);
    var data = {'action': eventObj['currentTarget']['id'], 'course_id': course_id};
    socket.emit('student_send', data)
});

$('.session_control').click(function (eventObj) {
    console.log(eventObj['currentTarget']['id']);
    var data = {'session_control': eventObj['currentTarget']['id'], 'course_id': course_id };
    socket.emit('lecturer_send', data)
});
