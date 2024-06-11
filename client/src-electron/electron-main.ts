import { app, BrowserWindow } from 'electron';
import path from 'path';
import os from 'os';
import { spawn } from 'child_process';

// needed in case process is undefined under Linux
const platform = process.platform || os.platform();

let mainWindow: BrowserWindow | undefined;

function createWindow() {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    icon: path.resolve(__dirname, 'icons/icon.png'), // tray icon
    width: 1000,
    height: 600,
    useContentSize: true,
    webPreferences: {
      contextIsolation: true,
      // More info: https://v2.quasar.dev/quasar-cli-vite/developing-electron-apps/electron-preload-script
      preload: path.resolve(__dirname, process.env.QUASAR_ELECTRON_PRELOAD),
    },
  });

  mainWindow.loadURL(process.env.APP_URL);

  if (process.env.DEBUGGING) {
    // if on DEV or Production with debug enabled
    mainWindow.webContents.openDevTools();
  } else {
    // we're on production; no access to devtools pls
    mainWindow.webContents.on('devtools-opened', () => {
      mainWindow?.webContents.closeDevTools();
    });
  }

  mainWindow.on('closed', () => {
    mainWindow = undefined;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === undefined) {
    createWindow();
  }
});

app.on('ready', () => {
  startFlaskServer();
});

function getBackendPath() {
  const config = require(path.join(__dirname, 'config.json'));
  return config.BackendPath
}

function startFlaskServer() {
  // Load 'config.json'
  console.log('CURRENT PATH: ' + __dirname);

  const config = require(path.join(__dirname, 'config.json'));

  const backendPath = config.BackendPath

  // alert with the current path
  console.log('BACKEND PATH: ' + backendPath);
  return;

  const flaskProcess = spawn('python', [path.join(__dirname, '../../flask_backend/app.py')]);

  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask stdout: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask stderr: ${data}`);
  });

  flaskProcess.on('close', (code) => {
    console.log(`Flask process exited with code ${code}`);
  });

  app.on('quit', () => {
    flaskProcess.kill();
  });
}
