import React from 'react';
import { Box, Button, Typography, useTheme } from '@mui/material';
import { keyframes } from '@emotion/react';

const errorGlitch = keyframes`
  0% {
    clip-path: inset(40% 0 61% 0);
    transform: translate(-20px, -10px);
  }
  20% {
    clip-path: inset(92% 0 1% 0);
    transform: translate(20px, 10px);
  }
  40% {
    clip-path: inset(43% 0 1% 0);
    transform: translate(3px, -30px);
  }
  60% {
    clip-path: inset(25% 0 58% 0);
    transform: translate(-15px, 15px);
  }
  80% {
    clip-path: inset(54% 0 7% 0);
    transform: translate(25px, -8px);
  }
  100% {
    clip-path: inset(58% 0 43% 0);
    transform: translate(-20px, -10px);
  }
`;

interface H4x0rErrorProps {
    error: string;
    onRetry?: () => void;
}

const H4x0rError: React.FC<H4x0rErrorProps> = ({ error, onRetry }) => {
    const theme = useTheme();

    return (
        <Box
            sx={{
                position: 'relative',
                width: '100%',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '2rem',
                backgroundColor: 'rgba(255,0,0,0.1)',
                border: '1px solid rgba(255,0,0,0.3)',
                overflow: 'hidden',
            }}
        >
            <Typography
                variant="h3"
                className="h4x0r-text"
                sx={{
                    color: theme.palette.error.main,
                    fontFamily: '"Share Tech Mono", monospace',
                    textAlign: 'center',
                    position: 'relative',
                    mb: 4,
                    '&::before, &::after': {
                        content: '"3RR0R_D3T3CT3D"',
                        position: 'absolute',
                        left: 0,
                        animation: `${errorGlitch} 3s infinite linear alternate-reverse`,
                        width: '100%',
                    },
                    '&::before': {
                        color: theme.palette.error.light,
                        clipPath: 'inset(45% 0 55% 0)',
                    },
                    '&::after': {
                        color: theme.palette.error.dark,
                        clipPath: 'inset(55% 0 45% 0)',
                    },
                }}
            >
                3RR0R_D3T3CT3D
            </Typography>

            <Box
                sx={{
                    position: 'relative',
                    padding: '1rem',
                    border: `1px solid ${theme.palette.error.main}`,
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    maxWidth: '80%',
                    mb: 4,
                    '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: `repeating-linear-gradient(
                            45deg,
                            transparent,
                            transparent 10px,
                            rgba(255,0,0,0.1) 10px,
                            rgba(255,0,0,0.1) 20px
                        )`,
                        animation: 'glitch 2s infinite',
                        pointerEvents: 'none',
                    },
                }}
            >
                <Typography
                    sx={{
                        color: theme.palette.error.main,
                        fontFamily: '"Share Tech Mono", monospace',
                        textAlign: 'center',
                        textShadow: `0 0 5px ${theme.palette.error.main}`,
                    }}
                >
                    {error}
                </Typography>
            </Box>

            {onRetry && (
                <Button
                    variant="outlined"
                    color="error"
                    onClick={onRetry}
                    sx={{
                        fontFamily: '"Share Tech Mono", monospace',
                        borderWidth: 2,
                        '&:hover': {
                            borderWidth: 2,
                            animation: 'glitch 1s infinite',
                            backgroundColor: 'rgba(255,0,0,0.1)',
                        },
                    }}
                >
                    R3TR1_3X3CUT3.exe
                </Button>
            )}

            <Box
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    pointerEvents: 'none',
                    '&::after': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '2px',
                        background: theme.palette.error.main,
                        animation: 'scanline 4s linear infinite',
                        opacity: 0.5,
                    },
                }}
            />
        </Box>
    );
};

export default H4x0rError; 