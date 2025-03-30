export const COLORS = {
    primary: '#00ff88',
    secondary: '#00e5ff',
    darkBg: '#0A0E17',
    darkPaper: '#141B2D',
    lightBg: '#f5f5f5',
    lightPaper: '#ffffff',
    accent: '#f7931a',  // Bitcoin orange
    success: '#3fb950',
    warning: '#d29922',
    error: '#f85149',
} as const;

export const GRADIENTS = {
    darkBackground: 'linear-gradient(180deg, #0A0E17 0%, #141B2D 100%)',
    lightBackground: 'linear-gradient(180deg, #f5f5f5 0%, #e0e0e0 100%)',
    primaryGlow: 'linear-gradient(45deg, #00ff88 30%, #00e5ff 90%)',
} as const;

export const SHADOWS = {
    card: '0 4px 20px rgba(0, 0, 0, 0.15)',
    glow: '0 0 10px rgba(0,255,136,0.5)',
} as const;

export const TRANSITIONS = {
    default: 'all 0.3s ease',
    slow: 'all 0.5s ease',
    fast: 'all 0.2s ease',
} as const;

export const Z_INDEX = {
    header: 1000,
    modal: 1300,
    tooltip: 1400,
    dropdown: 1200,
} as const; 