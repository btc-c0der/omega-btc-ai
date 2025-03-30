import React, { useState, useMemo } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { BrowserRouter as Router } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Portal from './components/Portal';

const App: React.FC = () => {
    const [darkMode, setDarkMode] = useState(true);

    const theme = useMemo(
        () =>
            createTheme({
                palette: {
                    mode: darkMode ? 'dark' : 'light',
                    primary: {
                        main: '#00ff88',
                    },
                    secondary: {
                        main: '#00e5ff',
                    },
                    background: {
                        default: darkMode ? '#0A0E17' : '#f5f5f5',
                        paper: darkMode ? '#141B2D' : '#ffffff',
                    },
                },
                typography: {
                    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
                },
                components: {
                    MuiCssBaseline: {
                        styleOverrides: {
                            body: {
                                scrollbarColor: darkMode ? '#6b6b6b #2b2b2b' : '#959595 #f5f5f5',
                                '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
                                    width: '8px',
                                },
                                '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
                                    borderRadius: 8,
                                    backgroundColor: darkMode ? '#6b6b6b' : '#959595',
                                    minHeight: 24,
                                },
                                '&::-webkit-scrollbar-track, & *::-webkit-scrollbar-track': {
                                    borderRadius: 8,
                                    backgroundColor: darkMode ? '#2b2b2b' : '#f5f5f5',
                                },
                            },
                        },
                    },
                },
            }),
        [darkMode]
    );

    const handleThemeToggle = () => setDarkMode(!darkMode);

    return (
        <Router>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <MainLayout darkMode={darkMode} onToggleTheme={handleThemeToggle}>
                    <Portal />
                </MainLayout>
            </ThemeProvider>
        </Router>
    );
};

export default App; 