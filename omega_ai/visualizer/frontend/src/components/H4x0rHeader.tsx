import React, { useEffect, useState } from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { keyframes } from '@emotion/react';

const glitch = keyframes`
  0% {
    clip-path: inset(71% 0 10% 0);
    transform: translate(-2px, 2px);
  }
  5% {
    clip-path: inset(24% 0 58% 0);
    transform: translate(2px, -2px);
  }
  10% {
    clip-path: inset(54% 0 10% 0);
    transform: translate(-1px, 1px);
  }
  15% {
    clip-path: inset(58% 0 43% 0);
    transform: translate(1px, -1px);
  }
  20% {
    clip-path: inset(24% 0 29% 0);
    transform: translate(-3px, 3px);
  }
  25% {
    clip-path: inset(13% 0 75% 0);
    transform: translate(3px, -3px);
  }
  30% {
    clip-path: inset(1% 0 88% 0);
    transform: translate(-1px, 1px);
  }
  35% {
    clip-path: inset(54% 0 36% 0);
    transform: translate(1px, -1px);
  }
  40% {
    clip-path: inset(15% 0 62% 0);
    transform: translate(-2px, 2px);
  }
  45% {
    clip-path: inset(89% 0 4% 0);
    transform: translate(2px, -2px);
  }
  50% {
    clip-path: inset(44% 0 33% 0);
    transform: translate(-3px, 3px);
  }
  55% {
    clip-path: inset(74% 0 19% 0);
    transform: translate(3px, -3px);
  }
  60% {
    clip-path: inset(23% 0 67% 0);
    transform: translate(-1px, 1px);
  }
  65% {
    clip-path: inset(48% 0 42% 0);
    transform: translate(1px, -1px);
  }
  70% {
    clip-path: inset(3% 0 69% 0);
    transform: translate(-2px, 2px);
  }
  75% {
    clip-path: inset(18% 0 71% 0);
    transform: translate(2px, -2px);
  }
  80% {
    clip-path: inset(54% 0 10% 0);
    transform: translate(-3px, 3px);
  }
  85% {
    clip-path: inset(31% 0 58% 0);
    transform: translate(3px, -3px);
  }
  90% {
    clip-path: inset(82% 0 4% 0);
    transform: translate(-1px, 1px);
  }
  95% {
    clip-path: inset(61% 0 25% 0);
    transform: translate(1px, -1px);
  }
  100% {
    clip-path: inset(100% 0 1% 0);
    transform: translate(0, 0);
  }
`;

const H4x0rHeader: React.FC = () => {
    const theme = useTheme();
    const [time, setTime] = useState(new Date().toLocaleTimeString());
    const [randomHex, setRandomHex] = useState('');

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date().toLocaleTimeString());
        }, 1000);

        const hexTimer = setInterval(() => {
            const hex = Math.random().toString(16).substr(2, 6).toUpperCase();
            setRandomHex(hex);
        }, 100);

        return () => {
            clearInterval(timer);
            clearInterval(hexTimer);
        };
    }, []);

    return (
        <Box
            sx={{
                position: 'relative',
                width: '100%',
                padding: '2rem',
                background: 'linear-gradient(180deg, rgba(0,255,65,0.1) 0%, rgba(0,0,0,0) 100%)',
                borderBottom: '1px solid rgba(0,255,65,0.3)',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                }}
            >
                <Typography
                    variant="h2"
                    className="h4x0r-text"
                    sx={{
                        fontFamily: '"Share Tech Mono", monospace',
                        color: theme.palette.primary.main,
                        position: 'relative',
                        '&::before, &::after': {
                            content: '"0M3G4 BTC TR4P V1SU4L1Z3R"',
                            position: 'absolute',
                            left: 0,
                            animation: `${glitch} 4s infinite`,
                            width: '100%',
                        },
                        '&::before': {
                            color: '#ff00ff',
                            clipPath: 'inset(45% 0 55% 0)',
                        },
                        '&::after': {
                            color: '#00ffff',
                            clipPath: 'inset(55% 0 45% 0)',
                        },
                    }}
                >
                    0M3G4 BTC TR4P V1SU4L1Z3R
                </Typography>
                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'flex-end',
                        fontFamily: '"Share Tech Mono", monospace',
                    }}
                >
                    <Typography
                        sx={{
                            color: theme.palette.primary.main,
                            fontSize: '1.2rem',
                        }}
                    >
                        {time}
                    </Typography>
                    <Typography
                        sx={{
                            color: theme.palette.secondary.main,
                            fontSize: '0.8rem',
                        }}
                    >
                        0x{randomHex}
                    </Typography>
                </Box>
            </Box>
            <Box
                sx={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    width: '100%',
                    height: '2px',
                    background: `linear-gradient(90deg, 
                        transparent 0%, 
                        ${theme.palette.primary.main} 50%, 
                        transparent 100%)`,
                    animation: 'scanline 2s linear infinite',
                }}
            />
        </Box>
    );
};

export default H4x0rHeader; 