import { createTheme } from '@mui/material';

export const cryptoTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#3C89E8', // Modern blue
            light: '#5BA2FF',
            dark: '#2B62B8',
            contrastText: '#FFFFFF',
        },
        secondary: {
            main: '#02C076', // Success green
            light: '#04D584',
            dark: '#019E61',
            contrastText: '#FFFFFF',
        },
        error: {
            main: '#FF5B5B',
            light: '#FF7A7A',
            dark: '#E53E3E',
        },
        warning: {
            main: '#FFB155',
            light: '#FFC178',
            dark: '#E59440',
        },
        info: {
            main: '#3C89E8',
            light: '#5BA2FF',
            dark: '#2B62B8',
        },
        success: {
            main: '#02C076',
            light: '#04D584',
            dark: '#019E61',
        },
        background: {
            default: '#0A0E17',
            paper: '#1C2230',
        },
        text: {
            primary: '#FFFFFF',
            secondary: '#A6B0C3',
        },
        divider: 'rgba(166, 176, 195, 0.1)',
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontWeight: 600,
            letterSpacing: '-0.5px',
        },
        h2: {
            fontWeight: 600,
            letterSpacing: '-0.5px',
        },
        h3: {
            fontWeight: 600,
        },
        h4: {
            fontWeight: 600,
        },
        h5: {
            fontWeight: 600,
        },
        h6: {
            fontWeight: 600,
        },
        subtitle1: {
            fontSize: '1rem',
            fontWeight: 500,
        },
        subtitle2: {
            fontWeight: 500,
        },
        body1: {
            fontSize: '0.875rem',
        },
        body2: {
            fontSize: '0.8125rem',
        },
    },
    shape: {
        borderRadius: 8,
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: `
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                
                body {
                    background-color: #0A0E17;
                    color: #FFFFFF;
                    font-family: "Inter", sans-serif;
                }

                ::-webkit-scrollbar {
                    width: 8px;
                    height: 8px;
                }

                ::-webkit-scrollbar-track {
                    background: #1C2230;
                }

                ::-webkit-scrollbar-thumb {
                    background: #2D3748;
                    border-radius: 4px;
                }

                ::-webkit-scrollbar-thumb:hover {
                    background: #3C4758;
                }
            `,
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                    backgroundColor: '#1C2230',
                    border: '1px solid rgba(166, 176, 195, 0.1)',
                    borderRadius: 12,
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none',
                    fontWeight: 600,
                    borderRadius: 8,
                    padding: '8px 16px',
                    '&:hover': {
                        boxShadow: '0 4px 12px rgba(60, 137, 232, 0.15)',
                    },
                },
                containedPrimary: {
                    background: 'linear-gradient(135deg, #3C89E8 0%, #2B62B8 100%)',
                },
                containedSecondary: {
                    background: 'linear-gradient(135deg, #02C076 0%, #019E61 100%)',
                },
            },
        },
        MuiTableCell: {
            styleOverrides: {
                root: {
                    borderColor: 'rgba(166, 176, 195, 0.1)',
                },
            },
        },
    },
}); 