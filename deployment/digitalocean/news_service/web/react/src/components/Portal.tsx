import React, { useState } from 'react';
import {
    Box,
    Grid,
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
    Article as ArticleIcon,
    Language as LanguageIcon,
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
                border: '1px solid rgba(0, 255, 136, 0.1)',
                '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: `0 0 20px ${theme.palette.primary.main}40`,
                    border: '1px solid rgba(0, 255, 136, 0.3)',
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
            title: 'Global News',
            description: 'Real-time crypto and financial news from around the world.',
            icon: <LanguageIcon />,
            path: '/news/global'
        },
        {
            title: 'Market Analysis',
            description: 'In-depth market analysis and expert insights.',
            icon: <ChartIcon />,
            path: '/news/analysis'
        },
        {
            title: 'AI Insights',
            description: 'AI-powered market predictions and pattern recognition.',
            icon: <AIIcon />,
            path: '/news/ai'
        },
        {
            title: 'P4NG34 Feed',
            description: 'Exclusive P4NG34 news and updates from the divine chronicles.',
            icon: <ArticleIcon />,
            path: '/news/pangea'
        },
        {
            title: 'Market Monitor',
            description: 'Real-time BTC market monitoring with trap detection.',
            icon: <MonitorIcon />,
            path: '/monitor'
        },
        {
            title: 'System Architecture',
            description: 'System overview and infrastructure management.',
            icon: <ArchitectureIcon />,
            path: '/architecture'
        },
        {
            title: 'Data Vortex',
            description: 'Interactive 3D visualization of market data patterns.',
            icon: <DataIcon />,
            path: '/vortex'
        },
        {
            title: 'Terminal',
            description: 'Advanced command interface for system control.',
            icon: <TerminalIcon />,
            path: '/terminal'
        },
        {
            title: 'Memory Architect',
            description: 'Manage and explore the immortal memory architecture.',
            icon: <MemoryIcon />,
            path: '/memory'
        },
        {
            title: 'Network Hub',
            description: 'Monitor network connections and data flow.',
            icon: <HubIcon />,
            path: '/network'
        },
        {
            title: 'Research Lab',
            description: 'Experimental features and research tools.',
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
                    mb: 4,
                    fontWeight: 'bold',
                    letterSpacing: '0.1em',
                    textShadow: '0 0 20px rgba(0, 255, 136, 0.5)'
                }}
            >
                P4NG34 NEWS PORTAL
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