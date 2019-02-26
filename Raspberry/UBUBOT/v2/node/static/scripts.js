function setMotorValue(id, value) {
    if (value >= 0) {
        document.getElementById(id + "-motor").style.width = value + "%";
        document.getElementById(id + "-motor").attributes.getNamedItem("aria-valuenow").value = value;
        document.getElementById(id + "-motor-reverse").style.width = "0";
        document.getElementById(id + "-motor-reverse").attributes.getNamedItem("aria-valuenow").value = 0;
    } else {
        document.getElementById(id + "-motor").style.width = "0";
        document.getElementById(id + "-motor").attributes.getNamedItem("aria-valuenow").value = 0;
        document.getElementById(id + "-motor-reverse").style.width = -value + "%";
        document.getElementById(id + "-motor-reverse").attributes.getNamedItem("aria-valuenow").value = -value;
    }
}

function appendLine(textbox, line) {
    var element = document.getElementById("textbox-" + textbox);
    var timestamp = document.createElement('span');
    var now = new Date();
    timestamp.innerHTML = '[' + pad(now.getHours(), 2) + ':' +
        pad(now.getMinutes(), 2) + ':' +
        pad(now.getSeconds(), 2) + '.' +
        pad(now.getMilliseconds(), 3) + ']';
    timestamp.classList.add("timestamp");
    var child_line = document.createElement('span');
    child_line.innerHTML = line;
    var child = document.createElement('div');
    child.appendChild(timestamp);
    child.appendChild(child_line);
    element.appendChild(child);
    element.scrollTop = element.scrollHeight;
}

function pad(number, size){
    return ("000" + number).substr(-size);
}

function toggleTimestamps() {
    textboxes = document.getElementsByClassName("textbox-log");
    for(var i = 0; i < textboxes.length; i++) {
        textboxes[i].classList.toggle("hidden-timestamps");
    }
}

$(function() {
    var socket = io();
    socket.on("ububot-serial", function(msg) {
        appendLine("serial", msg);
    });
    socket.on("ububot-function", f_json => {
        var f = JSON.parse(f_json);
        if (f.name == "turn_sharp") {
            if (f.direction == "left") {
                setMotorValue("left", -f.speed / 2);
                setMotorValue("right", f.speed / 2);
            } else {
                setMotorValue("left", f.speed / 2);
                setMotorValue("right", -f.speed / 2);
            }
        } else if (f.hasOwnProperty("speed")) {
            if (f.identifier == "L") {
                setMotorValue("left", f.speed / 2);
            } else if (f.identifier == "R") {
                setMotorValue("right", f.speed / 2);
            } else {
                setMotorValue("left", f.speed / 2);
                setMotorValue("right", f.speed / 2);
            }
        } else {
            setMotorValue("left", 0);
            setMotorValue("right", 0);
        }
        line = f.name + "(";

        var isFirst = true;
        for (var k in f) {
            if (k != "name") {
                if (!isFirst) line += ", ";
                else isFirst = false;
                line += f[k];
            }
        }
        line += ')';

        appendLine("functions", line);
    });
});
