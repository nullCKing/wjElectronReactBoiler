const { spawn } = require('child_process');
var path = require("path");
const { dialog } = require('electron');
var { PythonShell } = require('python-shell');

function selectDirectory(stateCheckboxes, 
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
            let scriptPath = path.join(__dirname, 'scraper.py');
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
            PythonShell.run(scriptPath, { 
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
            }, function(err) {
                if (err) throw err;
                console.log('File created!');
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