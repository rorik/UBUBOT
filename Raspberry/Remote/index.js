#!/usr/bin/env node

const exec = require("child_process");
const express = require("express");
const app = express();
const port = 5665;
const root = require("path").dirname(require.main.filename);

function run(script, retry = 3) {
    exec.exec(root + "/scripts/" + script, (err, _stdout, _stderr) => {
        return !err || retry > 0 && run(script, retry - 1);
    });
}

run("start.sh");

app.get("/reset", (_req, res) => {
    run("start.sh");
    res.status(200).send("OK");
});

app.get("/raise", (_req, res) => {
    run("raise.sh");
    res.status(200).send("OK");
});

app.get("/lower", (_req, res) => {
    run("lower.sh");
    res.status(200).send("OK");
});

app.get("/status", (_req, res) => {
    var lowered = exec.spawnSync(root + "/scripts/is_lowered.sh").stdout[0] == 48;
    var raised = exec.spawnSync(root + "/scripts/is_raised.sh").stdout[0] == 48;
    res.status(200).json({lowered: lowered, raised: raised});
});

app.listen(port, () => console.log(`Listening on port ${port} @ ${root}`));
