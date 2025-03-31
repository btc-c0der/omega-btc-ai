import React from 'react';
import { motion } from 'framer-motion';
import '../styles/FunkoCharacter.css';

export const FunkoCharacter: React.FC = () => {
    return (
        <motion.div
            className="funko-character"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.8, type: "spring" }}
        >
            <div className="funko-head">
                <div className="funko-face">
                    <div className="funko-eyes">
                        <div className="funko-eye left"></div>
                        <div className="funko-eye right"></div>
                    </div>
                    <div className="funko-mouth"></div>
                </div>
                <div className="funko-hair">
                    <div className="funko-hair-spike"></div>
                    <div className="funko-hair-spike"></div>
                    <div className="funko-hair-spike"></div>
                </div>
            </div>

            <div className="funko-body">
                <div className="funko-torso">
                    <div className="funko-shirt">
                        <div className="funko-shirt-design">🔱</div>
                    </div>
                </div>
                <div className="funko-arms">
                    <div className="funko-arm left"></div>
                    <div className="funko-arm right"></div>
                </div>
                <div className="funko-legs">
                    <div className="funko-leg left"></div>
                    <div className="funko-leg right"></div>
                </div>
            </div>

            <div className="funko-base">
                <div className="funko-stand"></div>
            </div>

            <div className="funko-glow"></div>
        </motion.div>
    );
}; 