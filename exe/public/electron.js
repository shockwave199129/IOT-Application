const { app, BrowserWindow, ipcMain } = require('electron');
const isDev = require('electron-is-dev');
const path = require('node:path');

//const { exec, spawn } = require('child_process');

require('@electron/remote/main').initialize()

function createWindow() {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true
        },
        autoHideMenuBar: true,
        fullscreenable: false,
        maximizable: false,
        title: 'IOT - Application',
    });

    // and load the index.html of the app.
    // win.loadFile("index.html");
    win.loadURL(
        isDev
            ? 'http://localhost:3000'
            : `file://${path.join(__dirname, '../build/index.html')}`
    );
    // Open the DevTools.
    if (isDev) {
        win.webContents.openDevTools({ mode: 'detach' });
    }

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bars to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('ready', () => {
    app.on('window-all-closed', () => {
        app.quit();
    });

    ipcMain.on('runScript', (event, scriptPath) => {
        const childProcess = spawn('python3', [path.join(scriptPath)]);
    
        childProcess.stdout.on('data', (data) => {
            event.reply('scriptData', data.toString());
        });
    
        childProcess.stderr.on('data', (data) => {
            console.error('Script error:', data.toString());
        });
    
        childProcess.on('close', (code) => {
            if (code !== 0) {
                console.error('Script exited with code:', code);
            }
        });
    });
    
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});