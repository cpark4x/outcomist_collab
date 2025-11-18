console.log('process.type:', process.type);
console.log('process.versions.electron:', process.versions.electron);
console.log('process.versions.node:', process.versions.node);
console.log('require.resolve("electron"):', require.resolve('electron'));

try {
  const electron = require('electron');
  console.log('typeof electron:', typeof electron);
  console.log('electron:', electron);
} catch (e) {
  console.log('Error requiring electron:', e.message);
}

if (process.type === 'browser') {
  console.log('Running in Electron main process!');
  const { app } = require('electron');
  app.whenReady().then(() => {
    console.log('Electron app ready!');
    app.quit();
  });
} else {
  console.log('NOT running in Electron process');
  process.exit(1);
}
