/**
 * Created by s on 22.02.17.
 */

var socket = io();
const timeOut = 15000;

socket.emit('join', {'course_id': course_id });

function enableAllButtons () {
        document.getElementById("slow").disabled = false;
        document.getElementById("fast").disabled = false;
        document.getElementById("easy").disabled = false;
        document.getElementById("hard").disabled = false;
}

function disableAllButtons () {
        document.getElementById("slow").disabled = true;
        document.getElementById("fast").disabled = true;
        document.getElementById("easy").disabled = true;
        document.getElementById("hard").disabled = true;
}

socket.on('student_recv', function (msg) {
    console.log(msg['active']);
    if(msg.hasOwnProperty('active')) {
        if(msg['active']) {
            enableAllButtons();
        } else {
            disableAllButtons();
        }
    }
});

function timeOutPace(){
    document.getElementById("slow").disabled = true;
    document.getElementById("fast").disabled = true;
    setTimeout(function() {
        document.getElementById("slow").disabled = false;
        document.getElementById("fast").disabled = false;
    }, timeOut);
}
document.getElementById("slow").addEventListener("click", timeOutPace);
document.getElementById("fast").addEventListener("click", timeOutPace);

function timeOutDifficulty(){
    document.getElementById("easy").disabled = true;
    document.getElementById("hard").disabled = true;
    setTimeout(function() {
        document.getElementById("easy").disabled = false;
        document.getElementById("hard").disabled = false;
    }, timeOut);
}
document.getElementById("easy").addEventListener("click", timeOutDifficulty);
document.getElementById("hard").addEventListener("click", timeOutDifficulty);

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

