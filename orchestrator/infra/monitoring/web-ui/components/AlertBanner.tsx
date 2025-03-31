import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import '../styles/AlertBanner.css';

interface AlertBannerProps {
    message: string;
    severity: 'warning' | 'critical' | 'info';
}

export const AlertBanner: React.FC<AlertBannerProps> = ({ message, severity }) => {
    return (
        <AnimatePresence>
            <motion.div
                className={`alert-banner ${severity}`}
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -50 }}
                transition={{ duration: 0.3 }}
            >
                <div className="alert-content">
                    <div className="alert-icon">
                        {severity === 'critical' && '⚠️'}
                        {severity === 'warning' && '🔔'}
                        {severity === 'info' && 'ℹ️'}
                    </div>
                    <div className="alert-message">{message}</div>
                </div>
                <div className="alert-border">
                    <div className="corner top-left"></div>
                    <div className="corner top-right"></div>
                    <div className="corner bottom-left"></div>
                    <div className="corner bottom-right"></div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}; 