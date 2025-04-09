/** @jsxImportSource @react-three/fiber */
import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF, Environment, ContactShadows } from '@react-three/drei';
import { motion } from 'framer-motion';
import Layout from '../components/layout/Layout';
import LoadingSpinner from '../components/ui/LoadingSpinner';

// Simple Bitcoin 3D model component
const BitcoinModel = () => {
    // In a real app, we would load an actual GLTF model
    // For now, we'll create a simple Bitcoin-like coin
    return (
        <group position={[0, 0, 0]} rotation={[0, Math.PI / 4, 0]}>
            {/* Main coin body */}
            <mesh castShadow receiveShadow>
                <cylinderGeometry args={[2, 2, 0.2, 32]} />
                <meshStandardMaterial
                    color="#f7931a"
                    metalness={0.8}
                    roughness={0.3}
                />
            </mesh>

            {/* Bitcoin logo */}
            <mesh position={[0, 0.11, 0]} rotation={[Math.PI / 2, 0, 0]}>
                <torusGeometry args={[1, 0.1, 16, 100]} />
                <meshStandardMaterial
                    color="#ffffff"
                    metalness={0.5}
                    roughness={0.2}
                />
            </mesh>

            {/* Center B */}
            <mesh position={[0, 0.12, 0]}>
                <torusGeometry args={[0.5, 0.1, 16, 100]} />
                <meshStandardMaterial
                    color="#ffffff"
                    metalness={0.5}
                    roughness={0.2}
                />
            </mesh>
        </group>
    );
};

// Bitcoin stats for the infographic
const bitcoinStats = [
    { label: 'Market Cap', value: '$1.24 trillion' },
    { label: 'Circulating Supply', value: '19,350,000 BTC' },
    { label: 'Maximum Supply', value: '21,000,000 BTC' },
    { label: 'Hash Rate', value: '456 EH/s' },
    { label: 'Mining Difficulty', value: '53.3 T' },
    { label: 'Block Time', value: '10 minutes' },
    { label: 'Halving Cycle', value: 'Every 210,000 blocks' },
    { label: 'Network Nodes', value: '15,000+' }
];

// Bitcoin timeline milestones
const bitcoinTimeline = [
    { year: 2008, event: 'Bitcoin whitepaper published by Satoshi Nakamoto' },
    { year: 2009, event: 'Genesis block mined' },
    { year: 2010, event: 'First Bitcoin transaction: 10,000 BTC for two pizzas' },
    { year: 2012, event: 'First halving event reduces block reward to 25 BTC' },
    { year: 2013, event: 'Bitcoin price surpasses $1,000 for the first time' },
    { year: 2016, event: 'Second halving event reduces block reward to 12.5 BTC' },
    { year: 2017, event: 'Bitcoin price reaches $20,000' },
    { year: 2020, event: 'Third halving event reduces block reward to 6.25 BTC' },
    { year: 2021, event: 'El Salvador adopts Bitcoin as legal tender' },
    { year: 2022, event: 'Bitcoin becomes official reserve asset for some nations' },
    { year: 2024, event: 'Fourth halving event reduces block reward to 3.125 BTC' }
];

const BitcoinInfoGraphic = () => {
    return (
        <Layout>
            <div className="space-y-10">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5 }}
                >
                    <h1 className="text-3xl font-bold mb-2">Bitcoin Infographic</h1>
                    <p className="text-lightText/70">
                        An interactive view of Bitcoin's key metrics and historical timeline.
                    </p>
                </motion.div>

                {/* 3D Bitcoin Visualization */}
                <motion.div
                    className="h-[400px] w-full bg-gradient-to-br from-dark to-secondary rounded-xl overflow-hidden shadow-xl"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                >
                    <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                        <ambientLight intensity={0.5} />
                        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />
                        <Suspense fallback={null}>
                            <BitcoinModel />
                            <Environment preset="city" />
                            <ContactShadows position={[0, -1, 0]} opacity={0.4} scale={5} blur={2.5} far={4} />
                        </Suspense>
                        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
                    </Canvas>
                </motion.div>

                {/* Key Bitcoin Stats */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.4 }}
                >
                    <h2 className="text-2xl font-semibold mb-4">Key Bitcoin Statistics</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {bitcoinStats.map((stat, index) => (
                            <motion.div
                                key={stat.label}
                                className="bg-dark rounded-lg p-4 text-center"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.3, delay: 0.1 * index }}
                            >
                                <p className="text-lightText/60 text-sm">{stat.label}</p>
                                <p className="text-xl font-bold text-primary mt-1">{stat.value}</p>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Historical Timeline */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.6 }}
                    className="mt-10"
                >
                    <h2 className="text-2xl font-semibold mb-4">Bitcoin Timeline</h2>
                    <div className="relative border-l-2 border-primary/30 pl-8 space-y-8 py-4">
                        {bitcoinTimeline.map((milestone, index) => (
                            <motion.div
                                key={milestone.year}
                                className="relative"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.5, delay: 0.1 * index }}
                            >
                                <div className="absolute -left-10 h-6 w-6 rounded-full bg-primary flex items-center justify-center text-xs text-darkBg font-bold">
                                    {index + 1}
                                </div>
                                <div className="bg-secondary/30 p-4 rounded-lg">
                                    <span className="text-primary font-bold">{milestone.year}</span>
                                    <p className="mt-1">{milestone.event}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Bitcoin Fun Facts */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.8 }}
                    className="bg-dark/50 rounded-xl p-6 mt-10"
                >
                    <h2 className="text-2xl font-semibold mb-4">Did You Know?</h2>
                    <ul className="space-y-3 list-disc pl-5">
                        <li>If you bought $100 of Bitcoin in 2010, it would be worth over $50 million today.</li>
                        <li>The final Bitcoin will be mined around the year 2140.</li>
                        <li>There are only 2,100 trillion satoshis (the smallest unit of Bitcoin) that will ever exist.</li>
                        <li>Lost Bitcoin is estimated to be around 20% of all Bitcoin that will ever exist.</li>
                        <li>The energy used to mine Bitcoin has driven innovation in renewable energy.</li>
                    </ul>
                </motion.div>
            </div>
        </Layout>
    );
};

export default BitcoinInfoGraphic; 