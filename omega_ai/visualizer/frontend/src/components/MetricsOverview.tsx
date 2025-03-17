import React from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { keyframes } from '@emotion/react';
import { useDataFeed } from '../hooks/useDataFeed';
import { MetricsData } from '../types/data';
import { SxProps, Theme } from '@mui/material/styles';

const dataGlow = keyframes`
  0% { text-shadow: 0 0 10px #00ff41; }
  50% { text-shadow: 0 0 20px #00ff41, 0 0 30px #00ff41; }
  100% { text-shadow: 0 0 10px #00ff41; }
`;

const rotate = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const scan = keyframes`
  0% { transform: translateY(-100%); opacity: 0.5; }
  100% { transform: translateY(100%); opacity: 0; }
`;

const containerStyles: SxProps<Theme> = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    position: 'relative',
    overflow: 'hidden',
};

const gridStyles: SxProps<Theme> = {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '1rem',
    mb: 2,
};

const MetricsOverview: React.FC = () => {
    const theme = useTheme();
    const { data: metrics, isLoading, error } = useDataFeed<MetricsData>('/api/metrics');

    if (isLoading) {
        return (
            <Box sx={containerStyles}>
                <Box sx={gridStyles}>
                    <MetricBox
                        label="1N1T14L1Z1NG"
                        value="..."
                        color={theme.palette.primary.main}
                    />
                    <MetricBox
                        label="C0NF1GUR1NG"
                        value="..."
                        color={theme.palette.primary.main}
                    />
                    <MetricBox
                        label="L04D1NG"
                        value="..."
                        color={theme.palette.primary.main}
                    />
                </Box>
                <Box
                    sx={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}
                >
                    <Box
                        sx={{
                            width: '200px',
                            height: '200px',
                            position: 'relative',
                            '&::before': {
                                content: '""',
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                right: 0,
                                bottom: 0,
                                border: `2px solid ${theme.palette.primary.main}`,
                                borderRadius: '50%',
                                animation: `${rotate} 2s linear infinite`,
                            },
                            '&::after': {
                                content: '""',
                                position: 'absolute',
                                top: -10,
                                left: -10,
                                right: -10,
                                bottom: -10,
                                border: `2px solid ${theme.palette.secondary.main}`,
                                borderRadius: '50%',
                                animation: `${rotate} 3s linear infinite reverse`,
                            },
                        }}
                    >
                        <Typography
                            sx={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                color: theme.palette.primary.main,
                                fontFamily: '"Share Tech Mono", monospace',
                                animation: `${dataGlow} 2s infinite`,
                            }}
                        >
                            1N1T14L1Z1NG...
                        </Typography>
                    </Box>
                </Box>
            </Box>
        );
    }

    if (error) {
        return (
            <Box
                sx={{
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: theme.palette.error.main,
                    fontFamily: '"Share Tech Mono", monospace',
                    animation: `${dataGlow} 2s infinite`,
                }}
            >
                3RR0R: {error?.message || 'UNK0WN_3RR0R'}
            </Box>
        );
    }

    const totalTraps = metrics?.totalTraps ?? 'N/4';
    const successRate = metrics?.successRate
        ? `${(metrics.successRate * 100).toFixed(1)}%`
        : 'N/4';
    const avgConfidence = metrics?.averageConfidence
        ? `${(metrics.averageConfidence * 100).toFixed(1)}%`
        : 'N/4';
    const trapsByType = metrics?.trapsByType || { bullish: 0, bearish: 0 };

    const bullishCount = trapsByType.bullish;
    const bearishCount = trapsByType.bearish;
    const total = bullishCount + bearishCount;
    const bullishPercentage = total > 0 ? (bullishCount / total) * 100 : 0;
    const bearishPercentage = total > 0 ? (bearishCount / total) * 100 : 0;

    return (
        <Box sx={containerStyles}>
            <Box sx={gridStyles}>
                <MetricBox
                    label="T0T4L_TR4PS"
                    value={totalTraps}
                    color={theme.palette.primary.main}
                />
                <MetricBox
                    label="SUCC3SS_R4T3"
                    value={successRate}
                    color={theme.palette.success.main}
                />
                <MetricBox
                    label="4VG_C0NF1D3NC3"
                    value={avgConfidence}
                    color={theme.palette.info.main}
                />
            </Box>

            <Box
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    position: 'relative',
                    padding: '1rem',
                }}
            >
                <Typography
                    variant="h6"
                    sx={{
                        fontFamily: '"Share Tech Mono", monospace',
                        color: theme.palette.primary.main,
                        mb: 2,
                        textAlign: 'center',
                        textShadow: `0 0 10px ${theme.palette.primary.main}`,
                    }}
                >
                    TR4P_D1STR1BUT10N.dat
                </Typography>

                <Box
                    sx={{
                        width: '200px',
                        height: '200px',
                        position: 'relative',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}
                >
                    {/* Background circle */}
                    <Box
                        sx={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            borderRadius: '50%',
                            border: `2px solid ${theme.palette.primary.main}`,
                            boxShadow: `0 0 20px ${theme.palette.primary.main}`,
                            '&::before': {
                                content: '""',
                                position: 'absolute',
                                top: -4,
                                left: -4,
                                right: -4,
                                bottom: -4,
                                borderRadius: '50%',
                                border: `1px solid ${theme.palette.primary.main}`,
                                opacity: 0.5,
                                animation: `${rotate} 10s linear infinite`,
                            },
                        }}
                    />

                    {/* Bearish segment */}
                    <Box
                        sx={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            clipPath: `polygon(50% 50%, 50% 0, ${50 + bearishPercentage / 2}% 0, 100% ${bearishPercentage}%, 50% 50%)`,
                            background: `linear-gradient(45deg, 
                                ${theme.palette.error.main} 0%,
                                ${theme.palette.error.dark} 100%
                            )`,
                            opacity: 0.7,
                            transform: 'rotate(90deg)',
                            filter: 'blur(1px)',
                        }}
                    />

                    {/* Bullish segment */}
                    <Box
                        sx={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            clipPath: `polygon(50% 50%, 50% 0, ${50 - bullishPercentage / 2}% 0, 0 ${bullishPercentage}%, 50% 50%)`,
                            background: `linear-gradient(-45deg, 
                                ${theme.palette.success.main} 0%,
                                ${theme.palette.success.dark} 100%
                            )`,
                            opacity: 0.7,
                            transform: 'rotate(-90deg)',
                            filter: 'blur(1px)',
                        }}
                    />

                    {/* Center dot */}
                    <Box
                        sx={{
                            width: '10px',
                            height: '10px',
                            borderRadius: '50%',
                            backgroundColor: theme.palette.primary.main,
                            boxShadow: `0 0 20px ${theme.palette.primary.main}`,
                            animation: `${dataGlow} 2s infinite`,
                        }}
                    />

                    {/* Scanning line */}
                    <Box
                        sx={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            height: '2px',
                            background: `linear-gradient(90deg, 
                                transparent 0%, 
                                ${theme.palette.primary.main} 50%, 
                                transparent 100%
                            )`,
                            animation: `${scan} 3s linear infinite`,
                            opacity: 0.5,
                        }}
                    />
                </Box>

                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        gap: '2rem',
                        mt: 2,
                    }}
                >
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                        }}
                    >
                        <Box
                            sx={{
                                width: '12px',
                                height: '12px',
                                backgroundColor: theme.palette.success.main,
                                boxShadow: `0 0 10px ${theme.palette.success.main}`,
                                animation: `${dataGlow} 2s infinite`,
                            }}
                        />
                        <Typography
                            sx={{
                                fontFamily: '"Share Tech Mono", monospace',
                                color: theme.palette.success.main,
                                textShadow: `0 0 5px ${theme.palette.success.main}`,
                            }}
                        >
                            BULL1SH: {bullishCount}
                        </Typography>
                    </Box>
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                        }}
                    >
                        <Box
                            sx={{
                                width: '12px',
                                height: '12px',
                                backgroundColor: theme.palette.error.main,
                                boxShadow: `0 0 10px ${theme.palette.error.main}`,
                                animation: `${dataGlow} 2s infinite`,
                            }}
                        />
                        <Typography
                            sx={{
                                fontFamily: '"Share Tech Mono", monospace',
                                color: theme.palette.error.main,
                                textShadow: `0 0 5px ${theme.palette.error.main}`,
                            }}
                        >
                            B34R1SH: {bearishCount}
                        </Typography>
                    </Box>
                </Box>
            </Box>

            {/* Grid overlay */}
            <Box
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: `
                        linear-gradient(rgba(0,255,65,0.05) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0,255,65,0.05) 1px, transparent 1px)
                    `,
                    backgroundSize: '20px 20px',
                    pointerEvents: 'none',
                    '&::after': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: 'radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.8) 100%)',
                        pointerEvents: 'none',
                    }
                }}
            />
        </Box>
    );
};

const MetricBox: React.FC<{ label: string; value: string | number; color: string }> = ({
    label,
    value,
    color,
}) => {
    return (
        <Box
            sx={{
                padding: '1rem',
                border: `1px solid ${color}`,
                backgroundColor: 'rgba(0,0,0,0.3)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    height: '1px',
                    background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
                },
                '&::after': {
                    content: '""',
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    width: '100%',
                    height: '2px',
                    background: `linear-gradient(90deg, 
                        transparent 0%, 
                        ${color} 50%, 
                        transparent 100%
                    )`,
                    animation: `${scan} 3s linear infinite`,
                },
            }}
        >
            <Typography
                sx={{
                    fontFamily: '"Share Tech Mono", monospace',
                    color,
                    fontSize: '0.8rem',
                    opacity: 0.8,
                }}
            >
                {label}
            </Typography>
            <Typography
                sx={{
                    fontFamily: '"Share Tech Mono", monospace',
                    color,
                    fontSize: '1.5rem',
                    fontWeight: 'bold',
                    animation: `${dataGlow} 2s infinite`,
                }}
            >
                {value}
            </Typography>
        </Box>
    );
};

export default MetricsOverview; 