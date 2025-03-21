import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { TrapProbabilityData } from '../types';

interface TrapProbabilityMeterProps {
    trapData: TrapProbabilityData | null;
}

const TrapProbabilityMeter: React.FC<TrapProbabilityMeterProps> = ({ trapData }) => {
    const [glowIntensity, setGlowIntensity] = useState('0 0 10px rgba(255, 61, 0, 0.5)');

    // Update glow intensity based on probability
    useEffect(() => {
        if (trapData && trapData.probability) {
            const probability = trapData.probability;

            if (probability > 0.7) {
                setGlowIntensity('0 0 20px rgba(255, 61, 0, 0.9)');
            } else if (probability > 0.5) {
                setGlowIntensity('0 0 15px rgba(255, 221, 0, 0.8)');
            } else if (probability > 0.3) {
                setGlowIntensity('0 0 10px rgba(255, 221, 0, 0.6)');
            } else {
                setGlowIntensity('0 0 5px rgba(0, 181, 45, 0.5)');
            }
        }
    }, [trapData]);

    if (!trapData) {
        return (
            <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
                <h2 className="text-xl font-display text-reggae-gold mb-2">TRAP PROBABILITY METER</h2>
                <div className="animate-pulse flex space-x-4">
                    <div className="rounded-full bg-reggae-black h-3 w-full"></div>
                </div>
                <p className="text-center mt-4 text-reggae-text/50">Loading trap data...</p>
            </div>
        );
    }

    // Calculate bar width based on probability
    const probability = trapData.probability;
    const barWidth = `${Math.min(probability * 100, 100)}%`;

    // Determine color based on probability
    const getBarColor = () => {
        if (probability > 0.7) return 'bg-reggae-red';
        if (probability > 0.5) return 'bg-reggae-orange';
        if (probability > 0.3) return 'bg-reggae-yellow';
        return 'bg-reggae-green';
    };

    // Format trend
    const formatTrend = (trend: string) => {
        if (!trend) return '';
        return trend.replace('_', ' ');
    };

    // Trend arrow
    const trendArrow = () => {
        const trend = trapData.trend || '';
        if (trend.includes('increasing')) {
            return <span className="text-reggae-red">↑</span>;
        } else if (trend.includes('decreasing')) {
            return <span className="text-reggae-green">↓</span>;
        }
        return <span className="text-reggae-yellow">↔</span>;
    };

    return (
        <div className="bg-reggae-black-light p-5 rounded-lg border border-reggae-gold/20">
            <h2 className="text-xl font-display text-reggae-gold mb-3 flex justify-between items-center">
                <span>TRAP PROBABILITY METER</span>
                <span className="text-sm font-mono">
                    {trendArrow()} {formatTrend(trapData.trend || '')}
                </span>
            </h2>

            {/* Main probability meter */}
            <div className="relative h-5 bg-reggae-black rounded-full overflow-hidden mb-3 border border-reggae-gold/30">
                <motion.div
                    className={`absolute top-0 left-0 h-full ${getBarColor()}`}
                    style={{ width: barWidth, boxShadow: glowIntensity }}
                    initial={{ width: '0%' }}
                    animate={{ width: barWidth }}
                    transition={{ duration: 0.5 }}
                />
            </div>

            <div className="flex justify-between items-center mb-4">
                <span className="text-xs text-reggae-text/70">LOW</span>
                <span className="text-xl font-mono font-bold">{(probability * 100).toFixed(1)}%</span>
                <span className="text-xs text-reggae-text/70">HIGH</span>
            </div>

            {/* Trap type if detected */}
            {trapData.trap_type && (
                <motion.div
                    className="mt-3 p-3 bg-reggae-black rounded-lg border border-reggae-red/50"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <div className="flex justify-between">
                        <span className="text-reggae-red font-mono">DETECTED PATTERN:</span>
                        <span className="text-reggae-gold">{(trapData.confidence * 100).toFixed(1)}% confidence</span>
                    </div>
                    <div className="text-xl text-reggae-yellow font-bold mt-1">
                        {trapData.trap_type.replace('_', ' ').toUpperCase()}
                    </div>
                </motion.div>
            )}

            {/* Component data details */}
            {trapData.components && (
                <div className="mt-4 space-y-2">
                    <h3 className="font-mono text-sm text-reggae-gold">COMPONENT ANALYSIS</h3>
                    {Object.entries(trapData.components).map(([key, component]) => (
                        <div key={key} className="flex items-center text-xs">
                            <div className="w-1/3 text-reggae-text/70">{key.replace('_', ' ')}</div>
                            <div className="w-2/3 flex items-center">
                                <div className="h-1 flex-grow bg-reggae-black rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-reggae-electric-blue"
                                        style={{ width: `${(component.value || 0) * 100}%` }}
                                    />
                                </div>
                                <span className="ml-2 font-mono">{((component.value || 0) * 100).toFixed(0)}%</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* JAH JAH alert message */}
            {trapData.message && (
                <motion.div
                    className="mt-4 p-3 bg-gradient-to-r from-reggae-green/20 via-reggae-yellow/20 to-reggae-red/20 rounded-lg border border-reggae-gold/30"
                    initial={{ scale: 0.95, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <p className="text-center text-reggae-gold font-display tracking-wide">
                        {trapData.message}
                    </p>
                </motion.div>
            )}
        </div>
    );
};

export default TrapProbabilityMeter; 