import React from 'react';
import { motion } from 'framer-motion';
import '../styles/MatrixPanel.css';

interface MatrixPanelProps {
    title: string;
    value: number;
    unit: string;
    trend: 'up' | 'down';
}

export const MatrixPanel: React.FC<MatrixPanelProps> = ({
    title,
    value,
    unit,
    trend
}) => {
    return (
        <motion.div
            className="matrix-panel"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="panel-header">
                <h3>{title}</h3>
                <div className={`trend-indicator ${trend}`}>
                    {trend === 'up' ? '📈' : '📉'}
                </div>
            </div>

            <div className="panel-content">
                <div className="value-display">
                    <span className="value">{value}</span>
                    <span className="unit">{unit}</span>
                </div>

                <div className="matrix-border">
                    <div className="corner top-left"></div>
                    <div className="corner top-right"></div>
                    <div className="corner bottom-left"></div>
                    <div className="corner bottom-right"></div>
                </div>
            </div>
        </motion.div>
    );
}; 