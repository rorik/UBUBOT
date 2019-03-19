var express = require("express");
var app = express();
var http = require("http").Server(app);
var io = require("socket.io")(http);
const si = require('systeminformation');

app.use('/lib', express.static('libjs'));
app.use(express.static('static'));

io.on("connection", socket => {
    var ip = socket.handshake.address;
    if (ip.startsWith("::ffff:")) {
        ip = ip.substring(7);
    }
    console.log(ip + " connected");
    socket.on("disconnect", () => {
        console.log(ip + " disconnected");
    });

    socket.on("ububot-serial", msg => {
        if (ip == "::1") socket.broadcast.emit("ububot-serial", msg);
        console.log("Serial: " + msg);
    });

    socket.on("ububot-function", msg => {
        if (ip == "::1") socket.broadcast.emit("ububot-function", msg);
        console.log("Function: " + msg);
    });

    socket.on("ububot-img", msg => {
        if (ip == "::1") socket.broadcast.emit("ububot-img", msg);
        console.log("Image");
    });
});

async function broadcastStatus() {
    try {
        const temp = await si.cpuTemperature();
        const cpu = await si.currentLoad();
        io.sockets.emit('ububot-status', {cpu: cpu.currentload, temp: temp.main});
    } catch (e) {
        console.error(e);
    }
}
setInterval(broadcastStatus, 500);

http.listen(80, function() {
    console.log("listening on *:80");
});
