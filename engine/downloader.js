var { PythonShell } = require('python-shell');
var path = require("path");
const { dialog } = require('electron');

function checkDependencies(event) {
    let scriptPath = path.join(__dirname, 'downloader.py');
    let pyshell = new PythonShell(scriptPath);

    pyshell.on('message', function (message) {
        event.reply('check-dependencies-reply', message);
    });

    pyshell.end(function (err) {
        if (err) {
            console.error(err);
        }
    });
}

module.exports = checkDependencies;