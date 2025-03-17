import React from 'react';
import { Box, CircularProgress } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import { useDataFeed } from '../hooks/useDataFeed';
import { TrapData } from '../types/data';

// Note: The 'complex union type' warning from MUI's sx prop typing is a known issue
// and can be safely ignored as it doesn't affect runtime behavior
const loadingStyles: SxProps<Theme> = {
    display: 'flex',
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
    const { data: traps, isLoading, error } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={errorStyles}>
                {error.message || 'UNK0WN_3RR0R'}
            </Box>
        );
    }

    if (!traps) {
        return (
            <Box sx={errorStyles}>
                N0_D4T4_F0UND.exe
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
                return `T1M3: ${day} ${hour.toString().padStart(2, '0')}:00\nTR4PS: ${value}`;
            },
            textStyle: {
                fontFamily: '"Share Tech Mono", monospace',
                color: '#00ff41',
            },
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            borderColor: '#00ff41',
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
                color: '#00ff41',
                fontFamily: '"Share Tech Mono", monospace',
            },
            axisLine: {
                lineStyle: {
                    color: '#00ff41',
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
                color: '#00ff41',
                fontFamily: '"Share Tech Mono", monospace',
            },
            axisLine: {
                lineStyle: {
                    color: '#00ff41',
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
                color: '#00ff41',
                fontFamily: '"Share Tech Mono", monospace',
            },
            inRange: {
                color: ['rgba(0, 255, 65, 0.2)', 'rgba(0, 255, 65, 1)'],
            },
        },
        series: [{
            name: 'TR4P_D3T3CT10NS',
            type: 'heatmap',
            data: data,
            label: {
                show: true,
                color: '#000',
                fontFamily: '"Share Tech Mono", monospace',
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 255, 65, 0.5)',
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
            {/* Matrix grid overlay */}
            <Box
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    pointerEvents: 'none',
                    background: `
                        linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px)
                    `,
                    backgroundSize: '20px 20px',
                }}
            />
        </Box>
    );
};

export default TrapDetectionMap; 