import { motion } from 'framer-motion';

interface MetricCardProps {
    title: string;
    value: string;
    icon?: string;
    trend?: 'up' | 'down' | 'neutral';
    trendValue?: string;
    additionalClass?: string;
    bgClass?: string;
}

const MetricCard = ({
    title,
    value,
    icon,
    trend,
    trendValue,
    additionalClass = '',
    bgClass = 'bg-dark'
}: MetricCardProps) => {
    return (
        <motion.div
            className={`${bgClass} rounded-xl p-4 shadow-lg hover:shadow-xl transition-shadow`}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            whileHover={{ y: -5 }}
        >
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-sm font-medium text-light/70">{title}</h3>
                {icon && <span className="text-xl">{icon}</span>}
            </div>

            <div className={`text-2xl font-bold mt-2 ${additionalClass}`}>
                {value}
            </div>

            {trend && trendValue && (
                <div className="flex items-center mt-2">
                    <span className={`text-xs flex items-center ${trend === 'up' ? 'text-success' :
                        trend === 'down' ? 'text-danger' : 'text-light/50'
                        }`}>
                        {trend === 'up' ? '↑ ' :
                            trend === 'down' ? '↓ ' : ''}
                        {trendValue}
                    </span>
                </div>
            )}
        </motion.div>
    );
};

export default MetricCard; 