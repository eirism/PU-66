/**
 * Created by Mathias on 15.02.17.
 */
const button_start = document.getElementById("button_start");
const button_stop = document.getElementById("button_stop");

button_start.onclick = function () {
    button_start.disabled = true;
    button_stop.disabled = false;
}

button_stop.onclick = function () {
    button_start.disabled = false;
    button_stop.disabled = true;
}