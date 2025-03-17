import React from 'react';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { h4x0rTheme } from './styles/H4x0rTheme';
import H4x0rHeader from './components/H4x0rHeader';
import PriceChart from './components/PriceChart';
import TrapDetectionMap from './components/TrapDetectionMap';
import MetricsOverview from './components/MetricsOverview';
import TrapPatterns3D from './components/TrapPatterns3D';

const App: React.FC = () => {
    return (
        <ThemeProvider theme={h4x0rTheme}>
            <CssBaseline />
            <Box
                sx={{
                    minHeight: '100vh',
                    background: 'linear-gradient(180deg, rgba(0,0,0,1) 0%, rgba(10,10,10,1) 100%)',
                }}
            >
                <H4x0rHeader />
                <Box
                    className="matrix-bg"
                    sx={{
                        padding: '2rem',
                        display: 'grid',
                        gap: '2rem',
                        gridTemplateColumns: 'repeat(2, 1fr)',
                        '& > *': {
                            className: 'neon-box',
                        },
                    }}
                >
                    <Box
                        sx={{
                            gridColumn: '1 / -1',
                            height: '400px',
                            padding: '1rem',
                        }}
                        className="neon-box"
                    >
                        <PriceChart />
                    </Box>
                    <Box
                        sx={{
                            height: '400px',
                            padding: '1rem',
                        }}
                        className="neon-box"
                    >
                        <TrapDetectionMap />
                    </Box>
                    <Box
                        sx={{
                            height: '400px',
                            padding: '1rem',
                        }}
                        className="neon-box"
                    >
                        <MetricsOverview />
                    </Box>
                    <Box
                        sx={{
                            gridColumn: '1 / -1',
                            height: '600px',
                            padding: '1rem',
                        }}
                        className="neon-box"
                    >
                        <TrapPatterns3D />
                    </Box>
                </Box>
            </Box>
        </ThemeProvider>
    );
};

export default App; 