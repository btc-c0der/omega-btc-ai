import React, { useEffect, useState } from 'react';
import { ServiceCard } from './ServiceCard';
import { useWebSocket } from '../../hooks/useWebSocket';
import { ServiceStatus } from '../../types/service';

// Divine service endpoints from our sacred infrastructure
const SACRED_ENDPOINTS = {
    websocket: 'ws://localhost:10091/health',
    matrix: 'http://localhost:10090/health',
    nginx: 'http://localhost:10083/ws/health'
};

export const ServiceGrid: React.FC = () => {
    const [services, setServices] = useState<ServiceStatus[]>([]);
    const wsStatus = useWebSocket(SACRED_ENDPOINTS.websocket);

    // Divine service monitoring
    useEffect(() => {
        const fetchServices = async () => {
            try {
                const response = await fetch(SACRED_ENDPOINTS.matrix);
                const data = await response.json();
                setServices(data.services);
            } catch (error) {
                console.error('Failed to fetch divine services:', error);
            }
        };

        fetchServices();
        const interval = setInterval(fetchServices, 5000); // Sacred refresh rate
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="divine-card">
            <h2 className="divine-title">
                🔱 OMEGA FUNKO MATRIX ORCHESTRATOR SURVEILLANCE GRID 🔱
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {services.map((service) => (
                    <ServiceCard
                        key={service.id}
                        service={service}
                        wsStatus={wsStatus}
                    />
                ))}
            </div>

            {/* Divine Status Summary */}
            <div className="mt-4 p-4 bg-rasta-green/10 rounded-lg">
                <h3 className="divine-subtitle">
                    🌟 Divine System Status ��
                </h3>
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-2 bg-rasta-green/20 rounded">
                        <span className="text-rasta-green">Active Services:</span>
                        <span className="ml-2 text-white">{services.filter(s => s.status === 'active').length}</span>
                    </div>
                    <div className="p-2 bg-rasta-green/20 rounded">
                        <span className="text-rasta-green">WebSocket Status:</span>
                        <span className={`ml-2 ${wsStatus ? 'text-rasta-green' : 'text-rasta-red'}`}>
                            {wsStatus ? 'Connected' : 'Disconnected'}
                        </span>
                    </div>
                    <div className="p-2 bg-rasta-green/20 rounded">
                        <span className="text-rasta-green">Last Update:</span>
                        <span className="ml-2 text-white">{new Date().toLocaleTimeString()}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}; 