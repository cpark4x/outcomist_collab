// List all available Electron bindings
console.log('Available bindings:');

if (process._linkedBinding) {
  console.log('\nTrying different binding names...');

  const bindingsToTry = [
    'electron',
    'atom_common_v8_util',
    'atom_browser_app',
    'atom_browser_window',
    'chrome_pdf',
  ];

  for (const name of bindingsToTry) {
    try {
      const binding = process._linkedBinding(name);
      console.log(`✓ ${name}:`, typeof binding, Object.keys(binding || {}).slice(0, 5));
    } catch (e) {
      console.log(`✗ ${name}: ${e.message}`);
    }
  }
}

// Try normal require
console.log('\nTrying normal require:');
try {
  const electron = require('electron');
  console.log('electron type:', typeof electron);
  if (typeof electron === 'object' && electron !== null) {
    console.log('electron.app:', typeof electron.app);
    console.log('Keys:', Object.keys(electron).slice(0, 10));
  }
} catch (e) {
  console.log('Error:', e.message);
}
