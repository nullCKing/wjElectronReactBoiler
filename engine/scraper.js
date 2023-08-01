const { spawn } = require('child_process');
var path = require("path");
const { dialog, Notification } = require('electron');
var { PythonShell } = require('python-shell');

let iconPath = path.join(__dirname, '../assets/icon.png');

const getPythonPath = (mainWindow, fileName) => {
    const path = require('path')
    const isDevBuild = process.env.NODE_ENV === 'development'

    let resolvedPath;
    if (isDevBuild) {
        resolvedPath = path.resolve(__dirname, `./${fileName}`)
    } else {
        const { app, remote } = require('electron')
        const appPath = app ? app.getAppPath() : remote.app.getAppPath()
        resolvedPath = path.resolve(appPath, `../engine/${fileName}`)
    }

    console.log('Resolved Python script path:', resolvedPath);
    mainWindow.webContents.executeJavaScript(`console.log('Resolved Python script path: ${resolvedPath.replace(/\\/g, '\\\\\\\\')}');`);
    return resolvedPath;
}
function selectDirectory(mainWindow, event, stateCheckboxes, 
    industryCheckboxes, 
    unlistedIndustry, 
    unlistedLocation, 
    unlistedPrice, 
    sunbeltNetwork, 
    synergy,       
    minGrossRevenue,
    maxGrossRevenue,
    minCashFlow,
    maxCashFlow,
    minListingPrice,
    maxListingPrice) {
    dialog.showOpenDialog({
        properties: ['openDirectory']
    }).then(result => {
        if (!result.canceled && result.filePaths.length > 0) {
            let directoryPath = result.filePaths[0];
            console.log("You selected: ", directoryPath);
            let scriptPath = getPythonPath(mainWindow, 'scraper.py');
            // serialize data to strings
            let stateCheckboxesString = JSON.stringify(stateCheckboxes);
            let industryCheckboxesString = JSON.stringify(industryCheckboxes);
            let unlistedIndustryString = JSON.stringify(unlistedIndustry);
            let unlistedLocationString = JSON.stringify(unlistedLocation);
            let unlistedPriceString = JSON.stringify(unlistedPrice);
            let sunbeltNetworkString = JSON.stringify(sunbeltNetwork);
            let synergyString = JSON.stringify(synergy);
            let minGrossRevenueString = JSON.stringify(minGrossRevenue);
            let maxGrossRevenueString = JSON.stringify(maxGrossRevenue);
            let minCashFlowString = JSON.stringify(minCashFlow);
            let maxCashFlowString = JSON.stringify(maxCashFlow);
            let minListingPriceString = JSON.stringify(minListingPrice);
            let maxListingPriceString = JSON.stringify(maxListingPrice);
            let pyshell = new PythonShell(scriptPath, { 
                args: [
                    directoryPath, 
                    stateCheckboxesString, 
                    industryCheckboxesString,
                    unlistedIndustryString,
                    unlistedLocationString,
                    unlistedPriceString,
                    sunbeltNetworkString,
                    synergyString,
                    minGrossRevenueString,
                    maxGrossRevenueString,
                    minCashFlowString,
                    maxCashFlowString,
                    minListingPriceString,
                    maxListingPriceString
                ] 
            });

            pyshell.on('message', function(message) {
                console.log('Message from Python:', message);
                let notification = new Notification({ title: 'Brokerage Search Tool', body: 'Background processes initiated', icon: iconPath });
                notification.show();
                // Handle the message from Python script
                if (message === 'DOWNLOAD_START') {
                  mainWindow.webContents.send('download-start');
                  let notification = new Notification({ title: 'Brokerage Search Tool', body: 'Download in progress. Please wait for the finished notification. This may take up to 60-90 minutes to complete.', icon: iconPath });
                  notification.show();
                } else if (message === 'DOWNLOAD_FINISH') {
                  mainWindow.webContents.send('download-finish');
                  let notification = new Notification({ title: 'Brokerage Search Tool', body: 'Download finished.', icon: iconPath });
                  notification.show();
                }
            });

            pyshell.on('error', function(err) {
                const fs = require('fs');
                const os = require('os');
                const path = require('path');
                const errorMsg = `Error occurred: ${err}\n${err.stack}\n`;
            
                const desktopDir = path.join(os.homedir(), 'Desktop');
                const logFilePath = path.join(desktopDir, 'errorLog.txt');
            
                fs.appendFile(logFilePath, errorMsg, function (err) {
                    if (err) throw err;
                    console.log(`Saved error message to ${logFilePath}`);
                });
            });    

            pyshell.end(function(err) {
                if (err) throw err;
                console.log('File created!');
                let notification = new Notification({ title: 'Brokerage Search Tool', body: 'File created!', icon: iconPath });
                notification.show();
                mainWindow.webContents.send('select-directory-reply', 'File created!');
            });
        }
        else
        {
            console.log("No directory selected.");
        }
    }).catch(err => {
        console.log(err);
    });
}

module.exports = {
    selectDirectory
};