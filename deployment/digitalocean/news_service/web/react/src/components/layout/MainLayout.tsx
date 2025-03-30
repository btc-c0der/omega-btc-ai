import React from 'react';
import { Box, Container, useTheme } from '@mui/material';
import Header from './Header';

interface MainLayoutProps {
    children: React.ReactNode;
    darkMode?: boolean;
    onToggleTheme?: () => void;
}

const MainLayout: React.FC<MainLayoutProps> = ({
    children,
    darkMode,
    onToggleTheme,
}) => {
    const theme = useTheme();

    return (
        <Box
            sx={{
                minHeight: '100vh',
                background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(180deg, #0A0E17 0%, #141B2D 100%)'
                    : 'linear-gradient(180deg, #f5f5f5 0%, #e0e0e0 100%)',
                py: 3,
                position: 'relative',
                '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'url("/pangea-bg-pattern.png")',
                    opacity: 0.05,
                    pointerEvents: 'none',
                },
            }}
        >
            <Header darkMode={darkMode} onToggleTheme={onToggleTheme} />
            <Container maxWidth="xl">
                <Box
                    sx={{
                        mt: 3,
                        position: 'relative',
                        zIndex: 1,
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
                    {children}
                </Box>
            </Container>
        </Box>
    );
};

export default MainLayout; 