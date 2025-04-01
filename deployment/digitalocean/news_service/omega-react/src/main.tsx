import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Removed StrictMode for better compatibility with Three.js
ReactDOM.createRoot(document.getElementById('root')!).render(
  <App />
)
