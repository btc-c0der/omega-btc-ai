import React, { useState } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    Card,
    CardContent,
    CardActionArea,
    IconButton,
    useTheme,
    Tooltip,
    Zoom,
} from '@mui/material';
import {
    MonitorHeart as MonitorIcon,
    ShowChart as ChartIcon,
    Psychology as AIIcon,
    Architecture as ArchitectureIcon,
    DataObject as DataIcon,
    Terminal as TerminalIcon,
    Memory as MemoryIcon,
    Hub as HubIcon,
    Biotech as BiotechIcon,
    Radar as RadarIcon,
} from '@mui/icons-material';

interface PortalCardProps {
    title: string;
    description: string;
    icon: React.ReactNode;
    path: string;
    onClick: () => void;
}

const PortalCard: React.FC<PortalCardProps> = ({ title, description, icon, onClick }) => {
    const theme = useTheme();

    return (
        <Card
            sx={{
                height: '100%',
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                transition: 'all 0.3s ease',
                '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: `0 0 20px ${theme.palette.primary.main}40`,
                    '& .MuiCardContent-root': {
                        background: `linear-gradient(45deg, ${theme.palette.primary.main}20, ${theme.palette.secondary.main}20)`,
                    }
                }
            }}
        >
            <CardActionArea onClick={onClick} sx={{ height: '100%' }}>
                <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                        <IconButton
                            sx={{
                                mr: 1,
                                color: theme.palette.primary.main,
                                background: theme.palette.primary.main + '10',
                            }}
                        >
                            {icon}
                        </IconButton>
                        <Typography variant="h6" component="div">
                            {title}
                        </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                        {description}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};

const Portal: React.FC = () => {
    const theme = useTheme();
    const [selectedModule, setSelectedModule] = useState<string | null>(null);

    const modules = [
        {
            title: 'Market Monitor',
            description: 'Real-time BTC market monitoring with advanced trap detection and visualization.',
            icon: <MonitorIcon />,
            path: '/monitor'
        },
        {
            title: 'Trading Dashboard',
            description: 'Advanced trading interface with real-time charts and order management.',
            icon: <ChartIcon />,
            path: '/trading'
        },
        {
            title: 'AI Models',
            description: 'Manage and monitor AI models for market prediction and pattern recognition.',
            icon: <AIIcon />,
            path: '/ai'
        },
        {
            title: 'System Architecture',
            description: 'System overview, component status, and infrastructure management.',
            icon: <ArchitectureIcon />,
            path: '/architecture'
        },
        {
            title: 'Data Vortex',
            description: 'Interactive 3D visualization of market data and trap patterns.',
            icon: <DataIcon />,
            path: '/vortex'
        },
        {
            title: 'Terminal',
            description: 'Advanced command interface for system control and debugging.',
            icon: <TerminalIcon />,
            path: '/terminal'
        },
        {
            title: 'Memory Architect',
            description: 'Manage and explore the system\'s immortal memory architecture.',
            icon: <MemoryIcon />,
            path: '/memory'
        },
        {
            title: 'Network Hub',
            description: 'Monitor and manage network connections and data flow.',
            icon: <HubIcon />,
            path: '/network'
        },
        {
            title: 'Research Lab',
            description: 'Experimental features and research tools for market analysis.',
            icon: <BiotechIcon />,
            path: '/research'
        },
        {
            title: 'Trap Radar',
            description: 'Advanced visualization of market manipulation patterns.',
            icon: <RadarIcon />,
            path: '/radar'
        }
    ];

    const handleModuleClick = (path: string) => {
        setSelectedModule(path);
        // Navigation logic will be implemented here
        console.log(`Navigating to ${path}`);
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography
                variant="h4"
                component="h1"
                gutterBottom
                sx={{
                    background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    textAlign: 'center',
                    mb: 4
                }}
            >
                OMEGA BTC AI Portal
            </Typography>

            <Grid container spacing={3}>
                {modules.map((module) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={module.path}>
                        <Tooltip
                            title={`Enter ${module.title}`}
                            TransitionComponent={Zoom}
                            arrow
                        >
                            <Box>
                                <PortalCard
                                    {...module}
                                    onClick={() => handleModuleClick(module.path)}
                                />
                            </Box>
                        </Tooltip>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default Portal; 