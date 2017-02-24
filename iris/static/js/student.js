const buttonSlow = document.getElementById("slow");
const buttonFast = document.getElementById("fast");
const buttonEasy = document.getElementById("easy");
const buttonHard = document.getElementById("hard");
const timeOut = 15000;

let socket = io();
socket.emit('join', {'course_id': courseID });

function enableAllButtons() {
        buttonSlow.disabled = false;
        buttonFast.disabled = false;
        buttonEasy.disabled = false;
        buttonHard.disabled = false;
}

function disableAllButtons() {
        buttonSlow.disabled = true;
        buttonFast.disabled = true;
        buttonEasy.disabled = true;
        buttonHard.disabled = true;
}

if(sessionActive){
    enableAllButtons();
}else{
    disableAllButtons();
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
    buttonSlow.disabled = true;
    buttonFast.disabled = true;
    setTimeout(function() {
        buttonSlow.disabled = false;
        buttonFast.disabled = false;
    }, timeOut);
}
buttonSlow.addEventListener("click", timeOutPace);
buttonFast.addEventListener("click", timeOutPace);

function timeOutDifficulty(){
    buttonEasy.disabled = true;
    buttonHard.disabled = true;
    setTimeout(function() {
        buttonEasy.disabled = false;
        buttonHard.disabled = false;
    }, timeOut);
}
buttonEasy.addEventListener("click", timeOutDifficulty);
buttonHard.addEventListener("click", timeOutDifficulty);

$('.action_button').click(function (eventObj) {
    console.log(eventObj['currentTarget']['id']);
    let data = {'action': eventObj['currentTarget']['id'], 'course_id': courseID};
    socket.emit('student_send', data);
});
