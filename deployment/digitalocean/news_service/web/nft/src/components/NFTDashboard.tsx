import React, { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Typography,
    Card,
    CardContent,
    IconButton,
    Tooltip,
    CircularProgress,
    Button,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
} from '@mui/material';
import {
    TrendingUp as TrendingUpIcon,
    ShowChart as ShowChartIcon,
    Timeline as TimelineIcon,
    Layers as LayersIcon,
    Assessment as AssessmentIcon,
    MonetizationOn as MonetizationOnIcon,
    AutoAwesome as AutoAwesomeIcon,
    Psychology as PsychologyIcon,
    Architecture as ArchitectureIcon,
} from '@mui/icons-material';

interface NFTMetrics {
    sacred_punks_count: number;
    divine_nfts_count: number;
    total_nfts: number;
}

interface GenerateResponse {
    success: boolean;
    image: string;
    metadata: string;
    error?: string;
}

const NFTDashboard: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [metrics, setMetrics] = useState<NFTMetrics | null>(null);
    const [openDialog, setOpenDialog] = useState(false);
    const [dialogType, setDialogType] = useState<'sacred-punk' | 'divine'>('sacred-punk');
    const [prompt, setPrompt] = useState('');
    const [generating, setGenerating] = useState(false);
    const [generatedNFT, setGeneratedNFT] = useState<GenerateResponse | null>(null);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await fetch('/api/nft/metrics');
            const data = await response.json();
            if (data.success) {
                setMetrics(data.metrics);
            }
        } catch (error) {
            console.error('Error fetching metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerate = async () => {
        setGenerating(true);
        try {
            const endpoint = dialogType === 'sacred-punk' ? '/api/nft/sacred-punk' : '/api/nft/divine';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    seed: Math.floor(Math.random() * 1000000),
                    prompt: dialogType === 'divine' ? prompt : undefined,
                }),
            });
            const data = await response.json();
            setGeneratedNFT(data);
            if (data.success) {
                fetchMetrics(); // Refresh metrics after generation
            }
        } catch (error) {
            console.error('Error generating NFT:', error);
            setGeneratedNFT({
                success: false,
                error: 'Failed to generate NFT',
                image: '',
                metadata: '',
            });
        } finally {
            setGenerating(false);
        }
    };

    const handleOpenDialog = (type: 'sacred-punk' | 'divine') => {
        setDialogType(type);
        setOpenDialog(true);
        setGeneratedNFT(null);
        setPrompt('');
    };

    const dashboardMetrics = [
        {
            title: 'Sacred Punks',
            value: metrics?.sacred_punks_count || 0,
            change: 'Active',
            icon: <AutoAwesomeIcon />,
            description: 'Generate unique Sacred Punk NFTs with divine traits',
            action: () => handleOpenDialog('sacred-punk'),
        },
        {
            title: 'Divine NFTs',
            value: metrics?.divine_nfts_count || 0,
            change: 'Active',
            icon: <PsychologyIcon />,
            description: 'Create divine NFTs with sacred geometry and cosmic energy',
            action: () => handleOpenDialog('divine'),
        },
        {
            title: 'Total Collection',
            value: metrics?.total_nfts || 0,
            change: 'Growing',
            icon: <LayersIcon />,
            description: 'Total NFTs in the sacred collection',
        },
        {
            title: 'Sacred Patterns',
            value: '8',
            change: 'Active',
            icon: <ArchitectureIcon />,
            description: 'Unique sacred geometry patterns available',
        },
        {
            title: 'Market Analysis',
            value: 'Live',
            change: 'Real-time',
            icon: <AssessmentIcon />,
            description: 'In-depth market analysis and divine metrics',
        },
        {
            title: 'Profit Calculator',
            value: 'Active',
            change: 'Updated',
            icon: <MonetizationOnIcon />,
            description: 'Calculate potential profits and divine alignment',
        },
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
                {dashboardMetrics.map((metric, index) => (
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
                                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                                    {metric.description}
                                </Typography>
                                {metric.action && (
                                    <Button
                                        variant="outlined"
                                        onClick={metric.action}
                                        sx={{
                                            color: '#00ff88',
                                            borderColor: '#00ff88',
                                            '&:hover': {
                                                borderColor: '#00e5ff',
                                                backgroundColor: 'rgba(0, 255, 136, 0.1)',
                                            }
                                        }}
                                    >
                                        Generate
                                    </Button>
                                )}
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Dialog
                open={openDialog}
                onClose={() => setOpenDialog(false)}
                maxWidth="md"
                fullWidth
            >
                <DialogTitle sx={{
                    background: 'linear-gradient(45deg, #00ff88, #00e5ff)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                }}>
                    {dialogType === 'sacred-punk' ? 'Generate Sacred Punk' : 'Create Divine NFT'}
                </DialogTitle>
                <DialogContent>
                    {dialogType === 'divine' && (
                        <TextField
                            fullWidth
                            label="Divine Prompt"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            margin="normal"
                            variant="outlined"
                            sx={{
                                '& .MuiOutlinedInput-root': {
                                    '& fieldset': {
                                        borderColor: 'rgba(0, 255, 136, 0.3)',
                                    },
                                    '&:hover fieldset': {
                                        borderColor: 'rgba(0, 255, 136, 0.5)',
                                    },
                                    '&.Mui-focused fieldset': {
                                        borderColor: '#00ff88',
                                    },
                                },
                            }}
                        />
                    )}
                    {generating ? (
                        <Box display="flex" justifyContent="center" p={3}>
                            <CircularProgress sx={{ color: '#00ff88' }} />
                        </Box>
                    ) : generatedNFT && (
                        <Box>
                            {generatedNFT.success ? (
                                <>
                                    <img
                                        src={generatedNFT.image}
                                        alt="Generated NFT"
                                        style={{ width: '100%', borderRadius: '8px', marginTop: '16px' }}
                                    />
                                    <Typography variant="body2" sx={{ mt: 2, color: '#00ff88' }}>
                                        NFT generated successfully! Check the metadata for divine metrics.
                                    </Typography>
                                </>
                            ) : (
                                <Typography color="error">
                                    {generatedNFT.error || 'Failed to generate NFT'}
                                </Typography>
                            )}
                        </Box>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button
                        onClick={() => setOpenDialog(false)}
                        sx={{ color: '#00ff88' }}
                    >
                        Close
                    </Button>
                    <Button
                        onClick={handleGenerate}
                        disabled={dialogType === 'divine' && !prompt || generating}
                        sx={{
                            color: '#00ff88',
                            '&:disabled': {
                                color: 'rgba(0, 255, 136, 0.3)',
                            },
                        }}
                    >
                        Generate
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default NFTDashboard;
