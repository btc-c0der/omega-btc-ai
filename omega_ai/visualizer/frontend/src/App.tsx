import React from 'react';
import { ThemeProvider, CssBaseline, Box, Container, Paper } from '@mui/material';
import { cryptoTheme } from './styles/CryptoTheme';
import Header from './components/Header';
import PriceChart from './components/PriceChart';
import TrapDetectionMap from './components/TrapDetectionMap';
import MetricsOverview from './components/MetricsOverview';
import TrapPatterns3D from './components/TrapPatterns3D';
import DataVortex from './components/CreativeDataVortex';

const App: React.FC = () => {
    return (
        <ThemeProvider theme={cryptoTheme}>
            <CssBaseline />
            <Box
                sx={{
                    minHeight: '100vh',
                    background: 'linear-gradient(180deg, #0A0E17 0%, #141B2D 100%)',
                    py: 3,
                }}
            >
                <Container maxWidth="xl">
                    <Header />
                    <Box
                        sx={{
                            display: 'grid',
                            gap: 3,
                            gridTemplateColumns: 'repeat(2, 1fr)',
                            '& > *': {
                                borderRadius: 2,
                                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
                                backdropFilter: 'blur(10px)',
                                backgroundColor: 'background.paper',
                                border: '1px solid',
                                borderColor: 'divider',
                            },
                        }}
                    >
                        <Paper
                            sx={{
                                gridColumn: '1 / -1',
                                height: '400px',
                                p: 2,
                            }}
                            elevation={0}
                        >
                            <PriceChart />
                        </Paper>
                        <Paper
                            sx={{
                                height: '400px',
                                p: 2,
                            }}
                            elevation={0}
                        >
                            <TrapDetectionMap />
                        </Paper>
                        <Paper
                            sx={{
                                height: '400px',
                                p: 2,
                            }}
                            elevation={0}
                        >
                            <MetricsOverview />
                        </Paper>
                        <Paper
                            sx={{
                                gridColumn: '1 / -1',
                                height: '600px',
                                p: 2,
                            }}
                            elevation={0}
                        >
                            <TrapPatterns3D />
                        </Paper>
                        <Paper
                            sx={{
                                gridColumn: '1 / -1',
                                height: '600px',
                                p: 2,
                            }}
                            elevation={0}
                        >
                            <DataVortex />
                        </Paper>
                    </Box>
                </Container>
            </Box>
        </ThemeProvider>
    );
};

export default App; 