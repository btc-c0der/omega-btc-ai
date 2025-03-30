import React, { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    Card,
    CardContent,
    IconButton,
    Tooltip,
    CircularProgress,
} from '@mui/material';
import {
    TrendingUp as TrendingUpIcon,
    ShowChart as ShowChartIcon,
    Timeline as TimelineIcon,
    Layers as LayersIcon,
    Assessment as AssessmentIcon,
    MonetizationOn as MonetizationOnIcon,
} from '@mui/icons-material';

const NFTDashboard: React.FC = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate data loading
        const timer = setTimeout(() => {
            setLoading(false);
        }, 2000);
        return () => clearTimeout(timer);
    }, []);

    const metrics = [
        {
            title: 'Floor Price Tracker',
            value: '2.5 ETH',
            change: '+12%',
            icon: <TrendingUpIcon />,
            description: 'Track floor prices across major NFT collections'
        },
        {
            title: 'Market Volume',
            value: '1.2K ETH',
            change: '+5%',
            icon: <ShowChartIcon />,
            description: 'Monitor NFT market trading volume'
        },
        {
            title: 'Price History',
            value: '30D',
            change: 'Active',
            icon: <TimelineIcon />,
            description: 'Historical price data and trends'
        },
        {
            title: 'Collections',
            value: '250+',
            change: 'Updated',
            icon: <LayersIcon />,
            description: 'Top NFT collections analytics'
        },
        {
            title: 'Market Analysis',
            value: 'Live',
            change: 'Real-time',
            icon: <AssessmentIcon />,
            description: 'In-depth market analysis and insights'
        },
        {
            title: 'Profit Calculator',
            value: 'Active',
            change: 'Updated',
            icon: <MonetizationOnIcon />,
            description: 'Calculate potential profits and losses'
        }
    ];

    if (loading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="100vh"
                sx={{
                    background: 'linear-gradient(180deg, #0A0E17 0%, #141B2D 100%)',
                }}
            >
                <CircularProgress
                    sx={{
                        color: '#00ff88',
                        '& .MuiCircularProgress-circle': {
                            strokeLinecap: 'round',
                        }
                    }}
                    size={60}
                />
            </Box>
        );
    }

    return (
        <Box sx={{ p: 3, minHeight: '100vh' }}>
            <Typography
                variant="h4"
                component="h1"
                gutterBottom
                sx={{
                    textAlign: 'center',
                    mb: 4,
                    background: 'linear-gradient(45deg, #00ff88, #00e5ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    textShadow: '0 0 20px rgba(0, 255, 136, 0.5)',
                    fontWeight: 'bold',
                    letterSpacing: '0.1em',
                }}
            >
                NFT Analytics Matrix
            </Typography>

            <Grid container spacing={3}>
                {metrics.map((metric, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                        <Card
                            sx={{
                                height: '100%',
                                background: 'rgba(255, 255, 255, 0.05)',
                                backdropFilter: 'blur(10px)',
                                transition: 'all 0.3s ease',
                                border: '1px solid rgba(0, 255, 136, 0.1)',
                                '&:hover': {
                                    transform: 'translateY(-5px)',
                                    boxShadow: '0 0 20px rgba(0, 255, 136, 0.3)',
                                    border: '1px solid rgba(0, 255, 136, 0.3)',
                                }
                            }}
                        >
                            <CardContent>
                                <Box display="flex" alignItems="center" mb={2}>
                                    <IconButton
                                        sx={{
                                            mr: 1,
                                            color: '#00ff88',
                                            background: 'rgba(0, 255, 136, 0.1)',
                                        }}
                                    >
                                        {metric.icon}
                                    </IconButton>
                                    <Typography variant="h6">
                                        {metric.title}
                                    </Typography>
                                </Box>
                                <Typography
                                    variant="h4"
                                    sx={{
                                        mb: 1,
                                        color: '#00ff88',
                                        textShadow: '0 0 10px rgba(0, 255, 136, 0.5)',
                                    }}
                                >
                                    {metric.value}
                                </Typography>
                                <Typography
                                    variant="body2"
                                    sx={{
                                        color: metric.change.includes('+') ? '#00ff88' : '#ffffff',
                                        mb: 2,
                                    }}
                                >
                                    {metric.change}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    {metric.description}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default NFTDashboard;
