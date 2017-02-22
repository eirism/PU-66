const button_slow = document.getElementById("slow");
const button_fast = document.getElementById("fast");
const button_easy = document.getElementById("easy");
const button_hard = document.getElementById("hard");
const timeOut = 15000;

let socket = io();
socket.emit('join', {'course_id': courseID });

function enableAllButtons() {
        button_slow.disabled = false;
        button_fast.disabled = false;
        button_easy.disabled = false;
        button_hard.disabled = false;
}

function disableAllButtons() {
        button_slow.disabled = true;
        button_fast.disabled = true;
        button_easy.disabled = true;
        button_hard.disabled = true;
}

socket.on('student_recv', function (msg) {
    console.log(msg['active']);
    if(msg.hasOwnProperty('active')) {
        if(msg['active']) {
            enableAllButtons();
        }else {
            disableAllButtons();
        }
    }
});

function timeOutPace(){
    button_slow.disabled = true;
    button_fast.disabled = true;
    setTimeout(function() {
        button_slow.disabled = false;
        button_fast.disabled = false;
    }, timeOut);
}
button_slow.addEventListener("click", timeOutPace);
button_fast.addEventListener("click", timeOutPace);

function timeOutDifficulty(){
    button_easy.disabled = true;
    button_hard.disabled = true;
    setTimeout(function() {
        button_easy.disabled = false;
        button_hard.disabled = false;
    }, timeOut);
}
button_easy.addEventListener("click", timeOutDifficulty);
button_hard.addEventListener("click", timeOutDifficulty);

$('form').submit(function(){
    let m_field = $('#m');
    let data = {'action': m_field.val()};
    console.log('Submitted: ' + data);
    socket.emit('student_send', data);
    m_field.val('');
    return false;
});

$('.action_button').click(function (eventObj) {
    console.log(eventObj['currentTarget']['id']);
    let data = {'action': eventObj['currentTarget']['id'], 'course_id': courseID};
    socket.emit('student_send', data)
});