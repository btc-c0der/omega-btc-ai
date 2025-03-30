import React from 'react';
import {
    AppBar,
    Toolbar,
    Typography,
    IconButton,
    Box,
    useTheme,
    Tooltip,
} from '@mui/material';
import {
    Brightness4 as DarkIcon,
    Brightness7 as LightIcon,
    Language as LanguageIcon,
} from '@mui/icons-material';

interface HeaderProps {
    darkMode?: boolean;
    onToggleTheme?: () => void;
}

const Header: React.FC<HeaderProps> = ({ darkMode, onToggleTheme }) => {
    const theme = useTheme();

    return (
        <AppBar position="static" color="transparent" elevation={0}>
            <Toolbar>
                <Box display="flex" alignItems="center" flex={1}>
                    <Typography
                        variant="h5"
                        sx={{
                            background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            fontWeight: 'bold',
                            letterSpacing: '0.1em',
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1,
                        }}
                    >
                        <LanguageIcon sx={{ color: theme.palette.primary.main }} />
                        P4NG34
                    </Typography>
                </Box>

                <Tooltip title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
                    <IconButton
                        onClick={onToggleTheme}
                        sx={{
                            color: theme.palette.primary.main,
                            '&:hover': {
                                background: theme.palette.primary.main + '20',
                            },
                        }}
                    >
                        {darkMode ? <LightIcon /> : <DarkIcon />}
                    </IconButton>
                </Tooltip>
            </Toolbar>
        </AppBar>
    );
};

export default Header; 