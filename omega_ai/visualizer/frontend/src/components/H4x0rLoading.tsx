import React, { useEffect, useRef } from 'react';
import { Box, useTheme } from '@mui/material';
import { keyframes } from '@emotion/react';

const pulse = keyframes`
  0% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.98); }
  100% { opacity: 1; transform: scale(1); }
`;

const rotate = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const H4x0rLoading: React.FC = () => {
    const theme = useTheme();
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        canvas.width = 200;
        canvas.height = 200;

        const matrix = '0123456789ABCDEF0M3G4TR4PBTCアイウエオカキクケコ';
        const drops: number[] = [];
        const fontSize = 10;
        const columns = canvas.width / fontSize;

        for (let i = 0; i < columns; i++) {
            drops[i] = 1;
        }

        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = theme.palette.primary.main;
            ctx.font = `${fontSize}px "Share Tech Mono"`;

            for (let i = 0; i < drops.length; i++) {
                const text = matrix[Math.floor(Math.random() * matrix.length)];
                const x = i * fontSize;
                const y = drops[i] * fontSize;

                ctx.shadowBlur = 3;
                ctx.shadowColor = theme.palette.primary.main;

                if (Math.random() < 0.1) {
                    ctx.fillStyle = theme.palette.secondary.main;
                } else if (Math.random() < 0.2) {
                    ctx.fillStyle = theme.palette.info.main;
                } else {
                    ctx.fillStyle = theme.palette.primary.main;
                }

                ctx.fillText(text, x, y);

                if (y > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }

                drops[i]++;
            }
        };

        const interval = setInterval(draw, 50);

        return () => {
            clearInterval(interval);
        };
    }, [theme]);

    return (
        <Box
            sx={{
                position: 'fixed',
                top: '20px',
                right: '20px',
                width: '200px',
                height: '200px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 9999,
            }}
        >
            <Box
                sx={{
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    border: `2px solid ${theme.palette.primary.main}`,
                    '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: -2,
                        left: -2,
                        right: -2,
                        bottom: -2,
                        border: `2px solid ${theme.palette.secondary.main}`,
                        animation: `${rotate} 4s linear infinite`,
                    },
                    '&::after': {
                        content: '""',
                        position: 'absolute',
                        top: -4,
                        left: -4,
                        right: -4,
                        bottom: -4,
                        border: `2px solid ${theme.palette.info.main}`,
                        animation: `${rotate} 6s linear infinite reverse`,
                    },
                }}
            />
            <canvas
                ref={canvasRef}
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    opacity: 0.8,
                }}
            />
            <Box
                sx={{
                    position: 'absolute',
                    padding: '0.5rem',
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    backdropFilter: 'blur(4px)',
                    border: `1px solid ${theme.palette.primary.main}`,
                    boxShadow: `0 0 10px ${theme.palette.primary.main}`,
                    animation: `${pulse} 2s infinite ease-in-out`,
                }}
            >
                <Box
                    component="span"
                    className="h4x0r-text"
                    sx={{
                        color: theme.palette.primary.main,
                        fontSize: '1rem',
                        fontFamily: '"Share Tech Mono", monospace',
                        textShadow: `0 0 5px ${theme.palette.primary.main}`,
                    }}
                >
                    PR0C3SS1NG...
                </Box>
            </Box>
        </Box>
    );
};

export default H4x0rLoading; 