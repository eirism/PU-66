/**
 * Created by Mathias on 15.02.17.
 */
const button_start = document.getElementById("button_start");
const button_stop = document.getElementById("button_stop");
const feedbackmsg = document.getElementById("lecturer_message")
let socket = io();
socket.emit('join', {'course_id': courseID});

if(sessionActive == "True"){
    button_start.disabled = true;
    button_stop.disabled = false;
}else{
    button_start.disabled = false;
    button_stop.disabled = true;
}

button_start.onclick = function () {
    button_start.disabled = true;
    button_stop.disabled = false;

    console.log("SESSION START");
    let data = {'session_control': 'start', 'course_id': courseID};
    socket.emit('lecturer_send', data);

    feedbackmsg.innerHTML = "Session started";
}

button_stop.onclick = function () {
    button_start.disabled = false;
    button_stop.disabled = true;

    console.log("SESSION STOP");
    let data = {'session_control': 'stop', 'course_id': courseID};
    socket.emit('lecturer_send', data);

    feedbackmsg.innerHTML = "Session stopped";
}

socket.on('lecturer_recv', function (msg) {
    console.log(msg['action']);
    $('#text_' + msg['action'][0]).html(msg['action'][1]);


});