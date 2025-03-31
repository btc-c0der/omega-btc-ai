import React from 'react';
import { ServiceStatus } from '../../types/service';

interface ServiceCardProps {
    service: ServiceStatus;
    wsStatus: boolean;
}

export const ServiceCard: React.FC<ServiceCardProps> = ({ service, wsStatus }) => {
    const getStatusClass = (status: string) => {
        switch (status.toLowerCase()) {
            case 'active':
                return 'divine-status-active';
            case 'warning':
                return 'divine-status-warning';
            case 'error':
                return 'divine-status-error';
            default:
                return 'divine-status';
        }
    };

    return (
        <div className="divine-card hover:border-rasta-green/40 transition-all">
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-rasta-green">
                    {service.name}
                </h3>
                <span className={`divine-status ${getStatusClass(service.status)}`}>
                    {service.status.toUpperCase()}
                </span>
            </div>

            <div className="space-y-2">
                <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Uptime:</span>
                    <span className="text-white">{service.uptime}</span>
                </div>

                <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Memory Usage:</span>
                    <span className="text-white">{service.memoryUsage}%</span>
                </div>

                <div className="flex justify-between text-sm">
                    <span className="text-gray-400">CPU Usage:</span>
                    <span className="text-white">{service.cpuUsage}%</span>
                </div>

                {service.lastError && (
                    <div className="mt-2 p-2 bg-rasta-red/20 rounded text-sm text-rasta-red">
                        {service.lastError}
                    </div>
                )}

                <div className="mt-2 pt-2 border-t border-rasta-green/10">
                    <div className="flex justify-between text-xs text-gray-500">
                        <span>Last Check:</span>
                        <span>{new Date(service.lastCheck).toLocaleTimeString()}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}; 