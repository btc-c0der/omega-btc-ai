import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html, Torus, Trail } from '@react-three/drei';
import { Box, CircularProgress, Typography } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';
import useDataFeed from '../hooks/useDataFeed';
import { PriceData, TrapData } from '../types/data';
import * as THREE from 'three';

const loadingStyles: SxProps<Theme> = {
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    width: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
};

interface VortexPointProps {
    position: [number, number, number];
    color: string;
    data: TrapData | PriceData;
    type: 'trap' | 'price';
}

const VortexPoint: React.FC<VortexPointProps> = ({ position, color, data, type }) => {
    const meshRef = useRef<THREE.Mesh>(null);
    const [hovered, setHovered] = useState(false);
    const intensity = hovered ? 1 : 0.5;

    useFrame((state) => {
        if (meshRef.current) {
            // Rotate the point around its axis
            meshRef.current.rotation.y += 0.02;
            // Add subtle floating motion
            meshRef.current.position.y += Math.sin(state.clock.elapsedTime * 2) * 0.002;
        }
    });

    return (
        <group position={position}>
            <mesh
                ref={meshRef}
                onPointerOver={() => setHovered(true)}
                onPointerOut={() => setHovered(false)}
            >
                {type === 'trap' ? (
                    <torusKnotGeometry args={[0.2, 0.05, 64, 8]} />
                ) : (
                    <dodecahedronGeometry args={[0.15]} />
                )}
                <meshPhongMaterial
                    color={color}
                    emissive={color}
                    emissiveIntensity={intensity}
                    shininess={100}
                />
            </mesh>
            {hovered && (
                <Html center>
                    <div style={{
                        background: 'rgba(0, 0, 0, 0.8)',
                        padding: '8px',
                        borderRadius: '4px',
                        color: '#fff',
                        fontSize: '12px',
                        whiteSpace: 'nowrap',
                        border: `1px solid ${color}`,
                        boxShadow: `0 0 10px ${color}`
                    }}>
                        {type === 'trap' ? (
                            <>
                                <div>Type: {(data as TrapData).type}</div>
                                <div>Confidence: {((data as TrapData).confidence * 100).toFixed(1)}%</div>
                            </>
                        ) : (
                            <>
                                <div>Price: ${(data as PriceData).close.toLocaleString()}</div>
                                <div>Change: {(((data as PriceData).close - (data as PriceData).open) / (data as PriceData).open * 100).toFixed(2)}%</div>
                            </>
                        )}
                        <div>Time: {new Date(type === 'trap' ? (data as TrapData).timestamp : (data as PriceData).time).toLocaleString()}</div>
                    </div>
                </Html>
            )}
        </group>
    );
};

const DataVortex: React.FC = () => {
    const { data: prices } = useDataFeed<PriceData[]>('/api/prices');
    const { data: traps, isLoading, error } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
                <Typography variant="body2" color="text.secondary">
                    Generating data vortex...
                </Typography>
            </Box>
        );
    }

    if (error || !traps || !prices) {
        return (
            <Box sx={loadingStyles}>
                <Typography color="error">
                    {error?.message || 'Failed to generate vortex'}
                </Typography>
            </Box>
        );
    }

    // Create a spiral pattern for data points
    const createSpiralPosition = (index: number, total: number, radius: number, height: number) => {
        const angle = (index / total) * Math.PI * 8; // 4 complete rotations
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const y = (index / total) * height - height / 2;
        return [x, y, z] as [number, number, number];
    };

    // Combine and sort data points by timestamp
    const combinedData = [
        ...traps.map(trap => ({ data: trap, type: 'trap' as const })),
        ...prices.map(price => ({ data: price, type: 'price' as const }))
    ].sort((a, b) => {
        const timeA = new Date(a.type === 'trap' ? a.data.timestamp : a.data.time).getTime();
        const timeB = new Date(b.type === 'trap' ? b.data.timestamp : b.data.time).getTime();
        return timeA - timeB;
    });

    return (
        <Canvas style={{ background: '#0a1929' }}>
            <OrbitControls enableDamping />
            <ambientLight intensity={0.3} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <spotLight
                position={[-10, 10, -10]}
                angle={0.5}
                penumbra={1}
                intensity={0.8}
                castShadow
            />

            {/* Energy field effect */}
            <Torus
                args={[8, 0.1, 16, 100]}
                rotation={[Math.PI / 2, 0, 0]}
            >
                <meshPhongMaterial
                    color="#1a90ff"
                    transparent
                    opacity={0.2}
                    wireframe
                />
            </Torus>

            {/* Data points in spiral formation */}
            {combinedData.map((item, index) => (
                <VortexPoint
                    key={item.type === 'trap' ? item.data.id : `price-${index}`}
                    position={createSpiralPosition(index, combinedData.length, 5, 10)}
                    color={item.type === 'trap'
                        ? (item.data as TrapData).type === 'bullish' ? '#52c41a' : '#ff4d4f'
                        : '#1a90ff'}
                    data={item.data}
                    type={item.type}
                />
            ))}

            {/* Legend */}
            <Html position={[-5, 4, 0]}>
                <div style={{
                    background: 'rgba(0, 0, 0, 0.8)',
                    padding: '12px',
                    borderRadius: '4px',
                    color: '#fff',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)'
                }}>
                    <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Data Vortex Legend:</div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div style={{ width: '12px', height: '12px', backgroundColor: '#52c41a', borderRadius: '50%' }}></div>
                            <div>Bullish Traps</div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div style={{ width: '12px', height: '12px', backgroundColor: '#ff4d4f', borderRadius: '50%' }}></div>
                            <div>Bearish Traps</div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div style={{ width: '12px', height: '12px', backgroundColor: '#1a90ff', borderRadius: '50%' }}></div>
                            <div>Price Points</div>
                        </div>
                    </div>
                </div>
            </Html>
        </Canvas>
    );
};

export default DataVortex; 