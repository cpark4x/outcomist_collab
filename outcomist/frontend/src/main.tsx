import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css';

// StrictMode removed to prevent double-mounting which causes duplicate session creation
ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
