const button_start = document.getElementById("button_start");
const button_stop = document.getElementById("button_stop");
const feedbackmsg = document.getElementById("lecturer_message");
let socket = io();
socket.emit('join', {'course_id': courseID});

function disableStart(){
    button_start.disabled = true;
    button_stop.disabled = false;
    feedbackmsg.innerHTML = "Session active";
}

function disableStop(){
    button_start.disabled = false;
    button_stop.disabled = true;
    feedbackmsg.innerHTML = "Session not active";
}

if(sessionActive == "True"){
    disableStart();
}else{
    disableStop();
}

button_start.onclick = function () {
    disableStart();

    console.log("SESSION START");
    let data = {'session_control': 'start', 'course_id': courseID};
    socket.emit('lecturer_send', data);
};

button_stop.onclick = function () {
    disableStop();

    console.log("SESSION STOP");
    let data = {'session_control': 'stop', 'course_id': courseID};
    socket.emit('lecturer_send', data);
};

socket.on('lecturer_recv', function (msg) {
    if(msg.hasOwnProperty('action')) {
        console.log(msg['action']);
        $('#text_' + msg['action'][0]).attr("data-badge", msg['action'][1]);
    }else if(msg.hasOwnProperty('active')) {
        console.log(msg['active']);
        if(msg['active']) {
            disableStart();
        }else {
            disableStop();
        }
    }
});
