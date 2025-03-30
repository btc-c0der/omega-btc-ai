import React, { useState, useMemo } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { BrowserRouter as Router } from 'react-router-dom';
import NFTDashboard from './components/NFTDashboard';

const App: React.FC = () => {
    const theme = useMemo(
        () =>
            createTheme({
                palette: {
                    mode: 'dark',
                    primary: {
                        main: '#00ff88',
                    },
                    secondary: {
                        main: '#00e5ff',
                    },
                    background: {
                        default: '#0A0E17',
                        paper: '#141B2D',
                    },
                },
                typography: {
                    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
                },
                components: {
                    MuiCssBaseline: {
                        styleOverrides: {
                            body: {
                                scrollbarColor: "#00ff88 #0A0E17",
                                "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
                                    backgroundColor: "#0A0E17",
                                },
                                "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
                                    borderRadius: 8,
                                    backgroundColor: "#00ff88",
                                    minHeight: 24,
                                    border: "3px solid #0A0E17",
                                },
                                "&::-webkit-scrollbar-thumb:focus, & *::-webkit-scrollbar-thumb:focus": {
                                    backgroundColor: "#00e5ff",
                                },
                                "&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active": {
                                    backgroundColor: "#00e5ff",
                                },
                                "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover": {
                                    backgroundColor: "#00e5ff",
                                },
                                "&::-webkit-scrollbar-corner, & *::-webkit-scrollbar-corner": {
                                    backgroundColor: "#0A0E17",
                                },
                            },
                        },
                    },
                },
            }),
        []
    );

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <NFTDashboard />
            </Router>
        </ThemeProvider>
    );
};

export default App;
