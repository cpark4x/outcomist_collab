const electron = require('electron');

console.log('electron type:', typeof electron);
console.log('electron value:', electron);
console.log('electron.app:', typeof electron.app);

if (electron.app) {
  electron.app.whenReady().then(() => {
    console.log('Electron app is ready!');
    electron.app.quit();
  });
} else {
  console.log('ERROR: electron.app is undefined!');
  process.exit(1);
}
