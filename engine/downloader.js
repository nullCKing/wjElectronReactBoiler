var { PythonShell } = require('python-shell');
var path = require("path");
const { app } = require('electron');
var fs = require("fs");

function checkDependencies(event) {
    let scriptPath = path.join(__dirname, 'downloader.py');
    let logPath = path.join(app.getPath('appData'), 'downloader-log.txt');

    function logToFile(message) {
        fs.appendFileSync(logPath, message + '\n');
    }

    logToFile("Attempting to check dependencies...");

    if (!fs.existsSync(scriptPath)) {
        let errorMsg = 'Python script not found at path:' + scriptPath;
        console.error(errorMsg);
        logToFile(errorMsg);
        return;
    }

    PythonShell.run(scriptPath, function (err) {
        if (err) {
            let errorMsg = 'Python shell error: ' + err;
            console.error(errorMsg);
            logToFile(errorMsg);
        }
        else {
            console.log("Dependencies checked successfully.");
            logToFile("Dependencies checked successfully.");
        }
    });
}

module.exports = checkDependencies;
