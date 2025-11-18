console.log('typeof process.electronBinding:', typeof process.electronBinding);
console.log('typeof global.require:', typeof global.require);
console.log('Object.keys(process):', Object.keys(process).filter(k => k.includes('electron') || k.includes('Electron')));

// Try to access electron through process
if (process.electron API) {
  console.log('Found process.electronAPI');
}

// Check what modules are available
console.log('typeof process._linkedBinding:', typeof process._linkedBinding);

// Try native modules
try {
  const { app } = process._linkedBinding('electron_common_app');
  console.log('Found app through _linkedBinding!');
  app.whenReady().then(() => {
    console.log('Success!');
    app.quit();
  });
} catch (e) {
  console.log('_linkedBinding failed:', e.message);
}
