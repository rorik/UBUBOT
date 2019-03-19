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

function clearTextbox(textbox) {
    var element = document.getElementById("textbox-" + textbox);
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
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

var lastImage = null;
function setImage(img) {
    var target = document.getElementById('stream-img');
    target.setAttribute('src', img);
    lastImage = new Date();
}

function resetImage() {
    var target = document.getElementById('stream-img');
    target.setAttribute('src', '/disconnected.png');
}

setInterval(function() {
    if (lastImage != null) {
        if (new Date().getTime() - lastImage.getTime() >= 5000) {
            resetImage();
        }
    }
}, 1000);

function reset() {
    clearTextbox('serial');
    clearTextbox('functions');
    resetImage();
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
    socket.on("ububot-img", img_json => {
        var img = JSON.parse(img_json);
        setImage('data:image/jpg;charset=utf-8;base64, ' + img.src);
    });
    socket.on("ububot-status", data => {
        var value;
        if ("cpu" in data && data.cpu >= 0) {
            value = Math.round(data.cpu);
            document.getElementById("status-cpu-bar").style.width = value + "%";
            document.getElementById("status-cpu-bar").attributes.getNamedItem("aria-valuenow").value = value;
            document.getElementById("status-cpu-value").innerText = value + '%';
        }
        if ("temp" in data && data.temp >= 0) {
            value = Math.round(data.temp/0.80);
            document.getElementById("status-temp-bar").style.width = value + "%";
            document.getElementById("status-temp-bar").attributes.getNamedItem("aria-valuenow").value = value;
            document.getElementById("status-temp-value").innerText = Math.round(data.temp) + '°C';
        }
    });
    socket.on("ububot-status-io", data_json => {
        data = JSON.parse(data_json);
        console.log(data);
        if ("type" in data) {
            switch (data.type.toLowerCase()) {
                case "sensor":
                    sensor = document.getElementById("sensor-" + data.name.toLowerCase());
                    if (sensor != null) {
                        if (!data.state) {
                            sensor.classList.add("active");
                        } else {
                            sensor.classList.remove("active");
                        }
                    }
                    break;
                case "relay":
                    relay = document.getElementById("relay-" + data.name.toLowerCase().replace('_', '-'));
                    if (relay != null) {
                        if (!data.state) {
                            relay.classList.add("active");
                        } else {
                            relay.classList.remove("active");
                        }
                    }
                    break;
                case "pwm":
                    pwm = document.getElementById("pwm-" + data.channel);
                    if (pwm != null) {
                        if (data.value) {
                            pwm.classList.add("active");
                        } else {
                            pwm.classList.remove("active");
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    });
});
