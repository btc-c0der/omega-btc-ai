import { motion } from 'framer-motion';
import useCosmicCycles from '../hooks/useCosmicCycles';

const CosmicCycleWidget = () => {
    const cycleData = useCosmicCycles();

    // Format time to next phase
    const formatNextPhaseTime = () => {
        const now = new Date();
        const diffMs = cycleData.nextPhaseTime.getTime() - now.getTime();
        const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

        return `${diffHrs}h ${diffMins}m`;
    };

    // Get color based on phase
    const getPhaseColor = () => {
        switch (cycleData.phase) {
            case 'new': return 'from-gray-800 to-indigo-900';
            case 'waxing': return 'from-indigo-800 to-primary';
            case 'full': return 'from-primary to-yellow-500';
            case 'waning': return 'from-gray-700 to-primary-dark';
            default: return 'from-gray-800 to-indigo-900';
        }
    };

    return (
        <motion.div
            className={`bg-gradient-to-br ${getPhaseColor()} rounded-xl p-4 shadow-lg relative overflow-hidden`}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
        >
            <div className="flex items-start justify-between mb-3">
                <div>
                    <h3 className="text-sm font-medium text-lightText/90">Cosmic Cycle</h3>
                    <p className="text-xs text-lightText/70">
                        Navigating the natural rhythms
                    </p>
                </div>
                <div className="h-12 w-12 flex items-center justify-center bg-darkBg/30 rounded-full backdrop-blur-sm">
                    <span className="text-3xl">{cycleData.phaseEmoji}</span>
                </div>
            </div>

            <div className="mt-3">
                <div className="flex justify-between items-center mb-1">
                    <span className="text-xs text-lightText/70">Phase Intensity</span>
                    <span className="text-xs font-bold text-lightText/90">{cycleData.intensity}%</span>
                </div>
                <div className="h-2 bg-darkBg/30 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-primary"
                        initial={{ width: 0 }}
                        animate={{ width: `${cycleData.intensity}%` }}
                        transition={{ duration: 1 }}
                    />
                </div>
            </div>

            <div className="mt-4">
                <div className="flex items-center gap-2 text-sm">
                    <span className="capitalize font-semibold">{cycleData.phase} Phase</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-darkBg/30">
                        Next: {formatNextPhaseTime()}
                    </span>
                </div>
                <p className="text-xs mt-1 text-lightText/80">
                    {cycleData.message}
                </p>
            </div>

            <div className="mt-3 pt-3 border-t border-lightText/10 flex justify-between items-center">
                <span className={`text-xs px-2 py-1 rounded-full ${cycleData.isFavorable
                    ? 'bg-success/20 text-success'
                    : 'bg-warning/20 text-warning'
                    }`}>
                    {cycleData.isFavorable ? 'Favorable Energy' : 'Cautious Energy'}
                </span>

                <motion.button
                    className="text-xs text-lightText/70 hover:text-lightText flex items-center gap-1"
                    whileHover={{ scale: 1.05 }}
                >
                    <span>Details</span>
                    <span>→</span>
                </motion.button>
            </div>

            {/* Decorative particles */}
            {[...Array(5)].map((_, i) => (
                <motion.div
                    key={i}
                    className="absolute w-1 h-1 rounded-full bg-primary/50"
                    style={{
                        top: `${10 + Math.random() * 80}%`,
                        left: `${10 + Math.random() * 80}%`,
                    }}
                    animate={{
                        opacity: [0.5, 1, 0.5],
                        scale: [1, 1.5, 1],
                    }}
                    transition={{
                        duration: 2 + Math.random() * 2,
                        repeat: Infinity,
                        delay: Math.random() * 2,
                    }}
                />
            ))}
        </motion.div>
    );
};

export default CosmicCycleWidget; 