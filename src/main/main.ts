/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import path from 'path';
import { app, BrowserWindow, dialog, shell, ipcMain } from 'electron';
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';
import { resolveHtmlPath } from './util';

// main.js (or whichever file you create the BrowserWindow in)
import { selectDirectory } from '../../engine/scraper.js';

log.transports.file.level = 'info';
autoUpdater.logger = log;

ipcMain.on('select-directory', (event, message, 
      stateCheckboxes, 
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
      maxListingPrice) => {
  try {
    // Pass stateCheckboxes, industryCheckboxes, and additional parameters
    const result = selectDirectory(stateCheckboxes, 
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
      maxListingPrice);
    // Send the result back to the renderer process
    event.reply('select-directory-reply', result);
  } catch (error) {
    console.error(error);
  }
});

class AppUpdater {
  constructor() {
    log.transports.file.level = 'info';
    autoUpdater.logger = log;
    this.setupListeners();
    autoUpdater.checkForUpdatesAndNotify();
    autoUpdater.on('checking-for-update', () => {
      log.info('Checking for update...');
    })
    
    autoUpdater.on('update-available', (info) => {
      log.info('Update available.', info);
      dialog.showMessageBox({
        type: 'info',
        buttons: ['Okay'],
        title: 'Title',
        message: 'Message text',
      });
    })
    
    autoUpdater.on('update-not-available', (info) => {
      log.info('Update not available.', info);
    })
    
    autoUpdater.on('error', (err) => {
      log.error('Error in auto-updater. ' + err);
    })
    
    autoUpdater.on('download-progress', (progressObj) => {
      let log_message = "Download speed: " + progressObj.bytesPerSecond;
      log_message = log_message + ' - Downloaded ' + progressObj.percent + '%';
      log_message = log_message + ' (' + progressObj.transferred + "/" + progressObj.total + ')';
      log.info(log_message);
    })
    
    autoUpdater.on('update-downloaded', (info) => {
      log.info('Update downloaded', info);
      dialog.showMessageBox({
        type: 'info',
        buttons: ['Okay'],
        title: 'Title',
        message: 'Message text',
      });
    });
  }

  setupListeners() {
    autoUpdater.on('update-available', () => {
      dialog.showMessageBox({
        type: 'info',
        title: 'Update available',
        message: 'A new version of the app is available. Do you want to update now?',
        buttons: ['Update', 'No']
      }).then(result => {
        let buttonIndex = result.response;
        if (buttonIndex === 0) {
          autoUpdater.downloadUpdate();
        }
      });
    });

    autoUpdater.on('update-downloaded', () => {
      dialog.showMessageBox({
        type: 'info',
        title: 'Update ready',
        message: 'Install and restart now?',
        buttons: ['Yes', 'Later']
      }).then(result => {
        let buttonIndex = result.response;
        if (buttonIndex === 0) {
          autoUpdater.quitAndInstall(false, true);
        }
      });
    });
  }
}

let mainWindow: BrowserWindow | null = null;

ipcMain.on('ipc-example', async (event, arg) => {
  const msgTemplate = (pingPong: string) => `IPC test: ${pingPong}`;
  console.log(msgTemplate(arg));
  event.reply('ipc-example', msgTemplate('pong'));
});

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

if (isDebug) {
  require('electron-debug')();
}

const installExtensions = async () => {
  const installer = require('electron-devtools-installer');
  const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
  const extensions = ['REACT_DEVELOPER_TOOLS'];

  return installer
    .default(
      extensions.map((name) => installer[name]),
      forceDownload
    )
    .catch(console.log);
};

const createWindow = async () => {
  if (isDebug) {
    await installExtensions();
  }

  const RESOURCES_PATH = app.isPackaged
    ? path.join(process.resourcesPath, 'assets')
    : path.join(__dirname, '../../assets');

  const getAssetPath = (...paths: string[]): string => {
    return path.join(RESOURCES_PATH, ...paths);
  };

  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    icon: getAssetPath('icon.png'),
    webPreferences: {
      preload: app.isPackaged
        ? path.join(__dirname, 'preload.js')
        : path.join(__dirname, '../../.erb/dll/preload.js'),
    },
  });

  mainWindow.maximize();

  mainWindow.loadURL(resolveHtmlPath('index.html'));

  mainWindow.on('ready-to-show', () => {
    if (!mainWindow) {
      throw new Error('"mainWindow" is not defined');
    }
    if (process.env.START_MINIMIZED) {
      mainWindow.minimize();
    } else {
      mainWindow.show();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });


  // Open urls in the user's browser
  mainWindow.webContents.setWindowOpenHandler((edata) => {
    shell.openExternal(edata.url);
    return { action: 'deny' };
  });

  // Remove this if your app does not use auto updates
  // eslint-disable-next-line
  new AppUpdater();
};

/**
 * Add event listeners...
 */

app.on('window-all-closed', () => {
  // Respect the OSX convention of having the application in memory even
  // after all windows have been closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});


app
  .whenReady()
  .then(() => {
    createWindow();
    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (mainWindow === null) createWindow();
    });
  })
  .catch(console.log);


