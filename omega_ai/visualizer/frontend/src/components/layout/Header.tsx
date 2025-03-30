import React from 'react';
import { AppBar, Toolbar, Typography, Box, IconButton } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';

interface HeaderProps {
    darkMode?: boolean;
    onToggleTheme?: () => void;
}

const Header: React.FC<HeaderProps> = ({ darkMode = true, onToggleTheme }) => {
    return (
        <AppBar position="static" color="transparent" elevation={0}>
            <Toolbar>
                <Box display="flex" alignItems="center" flex={1}>
                    <Typography
                        variant="h5"
                        sx={{
                            background: 'linear-gradient(45deg, #00ff88 30%, #00e5ff 90%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            fontWeight: 'bold',
                        }}
                    >
                        OMEGA BTC AI
                    </Typography>
                    <Typography
                        variant="subtitle2"
                        sx={{
                            ml: 2,
                            color: 'text.secondary',
                            borderLeft: '2px solid',
                            borderColor: 'divider',
                            pl: 2,
                        }}
                    >
                        Divine Blockchain Intelligence
                    </Typography>
                </Box>
                {onToggleTheme && (
                    <IconButton onClick={onToggleTheme} color="inherit">
                        {darkMode ? <Brightness7 /> : <Brightness4 />}
                    </IconButton>
                )}
            </Toolbar>
        </AppBar>
    );
};

export default Header; 