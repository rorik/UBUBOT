var app = require("express")();
var http = require("http").Server(app);
var io = require("socket.io")(http);

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/static/index.html");
});
app.get("/styles.css", function(req, res) {
    res.sendFile(__dirname + "/static/styles.css");
});
app.get("/scripts.js", function(req, res) {
    res.sendFile(__dirname + "/static/scripts.js");
});

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
});

http.listen(80, function() {
    console.log("listening on *:80");
});
