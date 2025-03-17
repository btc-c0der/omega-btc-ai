import { createTheme } from '@mui/material';

export const h4x0rTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#00ff41', // Matrix green
            light: '#00ff95',
            dark: '#00b833',
            contrastText: '#000000',
        },
        secondary: {
            main: '#ff00ff', // Cyberpunk pink
            light: '#ff66ff',
            dark: '#cc00cc',
            contrastText: '#000000',
        },
        error: {
            main: '#ff0000',
            light: '#ff3333',
            dark: '#cc0000',
        },
        warning: {
            main: '#ffff00',
            light: '#ffff33',
            dark: '#cccc00',
        },
        info: {
            main: '#00ffff',
            light: '#33ffff',
            dark: '#00cccc',
        },
        success: {
            main: '#00ff41',
            light: '#33ff70',
            dark: '#00cc35',
        },
        background: {
            default: '#0a0a0a',
            paper: '#1a1a1a',
        },
        text: {
            primary: '#00ff41',
            secondary: '#00b833',
        },
    },
    typography: {
        fontFamily: '"Share Tech Mono", "Roboto Mono", monospace',
        h1: {
            textShadow: '0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41',
        },
        h2: {
            textShadow: '0 0 8px #00ff41, 0 0 16px #00ff41',
        },
        h3: {
            textShadow: '0 0 6px #00ff41, 0 0 12px #00ff41',
        },
        h4: {
            textShadow: '0 0 4px #00ff41, 0 0 8px #00ff41',
        },
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: `@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

                /* Matrix rain effect */
                @keyframes glitch {
                    0% {
                        text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
                            0.025em 0.04em 0 #fffc00;
                    }
                    15% {
                        text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
                            0.025em 0.04em 0 #fffc00;
                    }
                    16% {
                        text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff,
                            -0.05em -0.05em 0 #fffc00;
                    }
                    49% {
                        text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff,
                            -0.05em -0.05em 0 #fffc00;
                    }
                    50% {
                        text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff,
                            0 -0.04em 0 #fffc00;
                    }
                    99% {
                        text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff,
                            0 -0.04em 0 #fffc00;
                    }
                    100% {
                        text-shadow: -0.05em 0 0 #00fffc, -0.025em -0.04em 0 #fc00ff,
                            -0.04em -0.025em 0 #fffc00;
                    }
                }

                @keyframes scanline {
                    0% {
                        transform: translateY(-100%);
                    }
                    100% {
                        transform: translateY(100%);
                    }
                }

                body {
                    background-color: #0a0a0a;
                    color: #00ff41;
                    font-family: "Share Tech Mono", monospace;
                    position: relative;
                    overflow-x: hidden;
                }

                body::before {
                    content: "";
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: repeating-linear-gradient(
                        0deg,
                        rgba(0, 255, 65, 0.03),
                        rgba(0, 255, 65, 0.03) 1px,
                        transparent 1px,
                        transparent 2px
                    );
                    pointer-events: none;
                }

                body::after {
                    content: "";
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(
                        rgba(0, 255, 65, 0.1),
                        rgba(0, 255, 65, 0.1)
                    );
                    animation: scanline 8s linear infinite;
                    pointer-events: none;
                }

                .h4x0r-text {
                    animation: glitch 3s infinite;
                }

                .neon-box {
                    border: 1px solid #00ff41;
                    box-shadow: 0 0 10px #00ff41, inset 0 0 10px #00ff41;
                    background: rgba(0, 255, 65, 0.05);
                }

                .matrix-bg {
                    background: 
                        linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
                    background-size: 20px 20px;
                }
            `,
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    background: 'rgba(10, 10, 10, 0.8)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid #00ff41',
                    boxShadow: '0 0 10px #00ff41, inset 0 0 10px #00ff41',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 0,
                    textTransform: 'uppercase',
                    fontFamily: '"Share Tech Mono", monospace',
                    '&:hover': {
                        animation: 'glitch 2s infinite',
                    },
                },
            },
        },
    },
}); 