import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import { useRealtimeDataFeed } from '../hooks/useRealtimeDataFeed';
import { TrapData } from '../types/data';

// Note: The 'complex union type' warning from MUI's sx prop typing is a known issue
// and can be safely ignored as it doesn't affect runtime behavior
const loadingStyles: SxProps<Theme> = {
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
};

const errorStyles: SxProps<Theme> = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    color: 'error.main',
    fontFamily: '"Share Tech Mono", monospace',
};

const TrapDetectionMap: React.FC = () => {
    const { data: traps, isConnected, error } = useRealtimeDataFeed<TrapData[]>('/ws/traps');

    if (!isConnected) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
                <Typography variant="body2" color="text.secondary">
                    Connecting to real-time data feed...
                </Typography>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={loadingStyles}>
                <Typography color="error">
                    {error.message || 'Failed to connect to real-time data feed'}
                </Typography>
            </Box>
        );
    }

    if (!traps) {
        return (
            <Box sx={loadingStyles}>
                <Typography color="text.secondary">
                    Waiting for trap detection data...
                </Typography>
            </Box>
        );
    }

    // Initialize the heatmap data array
    const data: [number, number, number][] = [];
    const hours = Array.from({ length: 24 }, (_, i) => i);
    const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

    // Count traps for each hour and day
    const trapCounts = new Map<string, number>();
    traps.forEach((trap: TrapData) => {
        const date = new Date(trap.timestamp);
        const day = date.getDay();
        const hour = date.getHours();
        const key = `${day}-${hour}`;
        trapCounts.set(key, (trapCounts.get(key) || 0) + 1);
    });

    // Fill the data array
    hours.forEach(hour => {
        days.forEach((_, day) => {
            data.push([hour, day, trapCounts.get(`${day}-${hour}`) || 0]);
        });
    });

    const chartOptions: EChartsOption = {
        backgroundColor: 'transparent',
        tooltip: {
            position: 'top',
            formatter: (params: any) => {
                const value = params.data[2];
                const day = days[params.data[1]];
                const hour = params.data[0];
                return `Time: ${day} ${hour.toString().padStart(2, '0')}:00\nTraps: ${value}`;
            },
        },
        grid: {
            top: '10%',
            left: '5%',
            right: '5%',
            bottom: '10%',
        },
        xAxis: {
            type: 'category',
            data: hours.map(h => h.toString().padStart(2, '0')),
            splitArea: {
                show: true,
            },
            axisLabel: {
                color: '#fff',
            },
            axisLine: {
                lineStyle: {
                    color: '#fff',
                },
            },
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true,
            },
            axisLabel: {
                color: '#fff',
            },
            axisLine: {
                lineStyle: {
                    color: '#fff',
                },
            },
        },
        visualMap: {
            min: 0,
            max: Math.max(...data.map(item => item[2])),
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '0%',
            textStyle: {
                color: '#fff',
            },
            inRange: {
                color: ['rgba(0, 146, 255, 0.2)', 'rgba(0, 146, 255, 1)'],
            },
        },
        series: [{
            name: 'Trap Detections',
            type: 'heatmap',
            data: data,
            label: {
                show: true,
                color: '#fff',
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 146, 255, 0.5)',
                },
            },
        }],
    };

    return (
        <Box sx={{ height: '100%', position: 'relative' }}>
            <ReactECharts
                option={chartOptions}
                style={{ height: '100%' }}
                theme="dark"
            />
            {/* Connection status indicator */}
            <Box
                sx={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                    padding: '4px 8px',
                    borderRadius: 1,
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                }}
            >
                <Box
                    sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        backgroundColor: isConnected ? '#52c41a' : '#ff4d4f',
                    }}
                />
                <Typography variant="caption" color="text.secondary">
                    {isConnected ? 'Live' : 'Disconnected'}
                </Typography>
            </Box>
        </Box>
    );
};

export default TrapDetectionMap; 