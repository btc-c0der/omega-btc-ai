import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';

// Components (to be created)
import PriceChart from './components/PriceChart';
import TrapDetectionMap from './components/TrapDetectionMap';
import MetricsOverview from './components/MetricsOverview';
import TrapPatterns3D from './components/TrapPatterns3D';
import TimelineView from './components/TimelineView';

// Create a dark theme
const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#0a1929',
            paper: '#132f4c',
        },
    },
    typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    },
});

const StyledPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
    height: 400,
    backgroundColor: 'rgba(19, 47, 76, 0.4)',
    backdropFilter: 'blur(10px)',
    borderRadius: theme.spacing(2),
    border: '1px solid rgba(255, 255, 255, 0.1)',
}));

function App() {
    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
                <AppBar position="static" elevation={0} sx={{ backgroundColor: 'rgba(19, 47, 76, 0.8)', backdropFilter: 'blur(10px)' }}>
                    <Toolbar>
                        <Typography variant="h5" component="h1" sx={{ flexGrow: 1 }}>
                            MM Trap Visualizer
                        </Typography>
                    </Toolbar>
                </AppBar>

                <Container maxWidth={false} sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
                    <Grid container spacing={3}>
                        {/* Price Chart */}
                        <Grid item xs={12} lg={8}>
                            <StyledPaper>
                                <Typography variant="h6" gutterBottom component="div">
                                    Price Movement & Traps
                                </Typography>
                                <PriceChart />
                            </StyledPaper>
                        </Grid>

                        {/* Metrics Overview */}
                        <Grid item xs={12} lg={4}>
                            <StyledPaper>
                                <Typography variant="h6" gutterBottom component="div">
                                    Metrics Overview
                                </Typography>
                                <MetricsOverview />
                            </StyledPaper>
                        </Grid>

                        {/* 3D Visualization */}
                        <Grid item xs={12} lg={8}>
                            <StyledPaper sx={{ height: 500 }}>
                                <Typography variant="h6" gutterBottom component="div">
                                    3D Trap Pattern Analysis
                                </Typography>
                                <TrapPatterns3D />
                            </StyledPaper>
                        </Grid>

                        {/* Timeline */}
                        <Grid item xs={12} lg={4}>
                            <StyledPaper sx={{ height: 500 }}>
                                <Typography variant="h6" gutterBottom component="div">
                                    Detection Timeline
                                </Typography>
                                <TimelineView />
                            </StyledPaper>
                        </Grid>

                        {/* Heat Map */}
                        <Grid item xs={12}>
                            <StyledPaper>
                                <Typography variant="h6" gutterBottom component="div">
                                    Trap Detection Heat Map
                                </Typography>
                                <TrapDetectionMap />
                            </StyledPaper>
                        </Grid>
                    </Grid>
                </Container>
            </Box>
        </ThemeProvider>
    );
}

export default App; 