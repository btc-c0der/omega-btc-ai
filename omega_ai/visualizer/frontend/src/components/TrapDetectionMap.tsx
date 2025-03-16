import React from 'react';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import { Box, CircularProgress } from '@mui/material';
import useDataFeed from '../hooks/useDataFeed';

const TrapDetectionMap: React.FC = () => {
    const { traps, loading, error } = useDataFeed();

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: 'error.main' }}>
                {error}
            </Box>
        );
    }

    // Process data for heatmap
    const hours = [...Array(24)].map((_, i) => i);
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    // Initialize data array with zeros
    const data: [number, number, number][] = [];
    const counts: number[][] = Array(7).fill(0).map(() => Array(24).fill(0));

    // Count traps for each hour and day
    traps.forEach(trap => {
        const date = new Date(trap.timestamp);
        const day = date.getDay();
        const hour = date.getHours();
        counts[day][hour] += 1;
    });

    // Convert counts to heatmap data format
    days.forEach((_, day) => {
        hours.forEach((hour) => {
            data.push([hour, day, counts[day][hour]]);
        });
    });

    const option: EChartsOption = {
        tooltip: {
            position: 'top',
            formatter: (params: any) => {
                const hour = params.data[0];
                const day = days[params.data[1]];
                const count = params.data[2];
                return `${day} ${hour}:00<br/>Traps detected: ${count}`;
            }
        },
        grid: {
            height: '50%',
            top: '10%'
        },
        xAxis: {
            type: 'category',
            data: hours.map(h => `${h}:00`),
            splitArea: {
                show: true
            }
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true
            }
        },
        visualMap: {
            min: 0,
            max: Math.max(...data.map(d => d[2])),
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '15%',
            textStyle: {
                color: '#fff'
            }
        },
        series: [{
            name: 'Trap Detections',
            type: 'heatmap',
            data: data,
            label: {
                show: true
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };

    return (
        <ReactECharts
            option={option}
            style={{ height: '100%', minHeight: '300px' }}
            theme="dark"
        />
    );
};

export default TrapDetectionMap; 