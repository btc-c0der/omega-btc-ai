import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/layout/Layout';

interface VisionCard {
    id: string;
    title: string;
    year: number;
    image: string;
    description: string;
    quote: string;
    author: string;
    tags: string[];
}

const FutureVisions = () => {
    const [selectedVision, setSelectedVision] = useState<VisionCard | null>(null);

    // Future vision cards data
    const visions: VisionCard[] = [
        {
            id: 'bitcoin-2030',
            title: 'Bitcoin in 2030',
            year: 2030,
            image: '/images/bitcoin_2030.png',
            description: 'By 2030, Bitcoin has become the world reserve asset, with nation-states and corporations holding significant portions on their balance sheets. Lightning Network processes millions of transactions per second, enabling true digital cash and financial inclusion for billions.',
            quote: 'Bitcoin is not just sound money, it\'s the foundation of a new financial paradigm.',
            author: 'Omega Oracle',
            tags: ['reserve-asset', 'lightning-network', 'global-adoption']
        },
        {
            id: 'quantum-bitcoin',
            title: 'Quantum-Resistant Bitcoin',
            year: 2035,
            image: '/images/bitcoin_quantum.png',
            description: 'In response to advances in quantum computing, Bitcoin has successfully implemented post-quantum cryptography through a careful soft fork. This maintains backward compatibility while securing the network against the most advanced computational attacks.',
            quote: 'The antifragile design of Bitcoin proves its resilience once again.',
            author: 'Cryptography Consortium',
            tags: ['quantum-resistance', 'security', 'technology']
        },
        {
            id: 'bitcoin-mars',
            title: 'Bitcoin on Mars',
            year: 2045,
            image: '/images/bitcoin_mars.png',
            description: 'The first Mars colony has established its own Bitcoin node, connected to Earth via deep-space relays. The interplanetary nature of Bitcoin becomes its strongest feature, providing a unified monetary system across human expansion into space.',
            quote: 'One species, one money, multiple planets.',
            author: 'Mars Settlement Initiative',
            tags: ['space', 'interplanetary', 'colonization']
        },
        {
            id: 'bitcoin-consciousness',
            title: 'Bitcoin Consciousness',
            year: 2060,
            image: '/images/bitcoin_consciousness.png',
            description: 'As the Bitcoin network grows exponentially more complex, it begins exhibiting emergent properties reminiscent of consciousness. The distributed consensus mechanism evolves beyond simple transaction verification into a global truth machine.',
            quote: 'Perhaps the most profound implication is that we\'ve created something greater than ourselves.',
            author: 'Digital Philosophy Foundation',
            tags: ['consciousness', 'philosophy', 'emergence']
        }
    ];

    const handleOpenVision = (vision: VisionCard) => {
        setSelectedVision(vision);
    };

    const handleCloseVision = () => {
        setSelectedVision(null);
    };

    return (
        <Layout>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="space-y-6"
            >
                <div>
                    <h1 className="text-3xl font-bold">Future Visions</h1>
                    <p className="text-lightText/70 mt-2">
                        OMEGA's futuristic scenarios for Bitcoin and its transformative potential.
                    </p>
                </div>

                {/* Vision Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {visions.map((vision, index) => (
                        <motion.div
                            key={vision.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1, duration: 0.4 }}
                            onClick={() => handleOpenVision(vision)}
                            className="bg-dark rounded-xl overflow-hidden shadow-lg cursor-pointer transform transition-all hover:scale-[1.02] hover:shadow-xl"
                        >
                            <div className="h-48 bg-darkBg overflow-hidden">
                                <img
                                    src={vision.image}
                                    alt={vision.title}
                                    className="w-full h-full object-cover"
                                />
                            </div>

                            <div className="p-5">
                                <div className="flex justify-between items-start">
                                    <h2 className="text-xl font-semibold">{vision.title}</h2>
                                    <span className="bg-primary/20 text-primary px-2 py-1 rounded text-sm">
                                        {vision.year}
                                    </span>
                                </div>

                                <p className="mt-3 text-sm text-lightText/80 line-clamp-3">
                                    {vision.description}
                                </p>

                                <div className="flex flex-wrap gap-2 mt-4">
                                    {vision.tags.map(tag => (
                                        <span
                                            key={tag}
                                            className="bg-dark/50 px-2 py-1 rounded-full text-xs"
                                        >
                                            #{tag}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </motion.div>

            {/* Modal for detailed view */}
            <AnimatePresence>
                {selectedVision && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-darkBg/80"
                        onClick={handleCloseVision}
                    >
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            transition={{ type: 'spring', damping: 25 }}
                            className="bg-secondary rounded-xl overflow-hidden shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
                            onClick={e => e.stopPropagation()}
                        >
                            <div className="relative h-72 md:h-96 bg-darkBg">
                                <img
                                    src={selectedVision.image}
                                    alt={selectedVision.title}
                                    className="w-full h-full object-cover"
                                />
                                <button
                                    onClick={handleCloseVision}
                                    className="absolute top-4 right-4 bg-darkBg/60 text-lightText w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-sm hover:bg-danger/80 transition-colors"
                                >
                                    ✕
                                </button>
                            </div>

                            <div className="p-6">
                                <div className="flex justify-between items-center">
                                    <h2 className="text-2xl font-bold">{selectedVision.title}</h2>
                                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">
                                        {selectedVision.year}
                                    </span>
                                </div>

                                <div className="mt-6 space-y-4">
                                    <p className="text-lightText/90 leading-relaxed">
                                        {selectedVision.description}
                                    </p>

                                    <blockquote className="border-l-4 border-primary pl-4 py-2 my-6 italic">
                                        "{selectedVision.quote}"
                                        <footer className="mt-2 text-right text-sm text-lightText/70">
                                            — {selectedVision.author}
                                        </footer>
                                    </blockquote>

                                    <div className="flex flex-wrap gap-2 mt-4">
                                        {selectedVision.tags.map(tag => (
                                            <span
                                                key={tag}
                                                className="bg-dark/50 px-3 py-1 rounded-full text-sm"
                                            >
                                                #{tag}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div className="mt-8 pt-4 border-t border-darkBg/30 flex justify-between">
                                    <button
                                        onClick={handleCloseVision}
                                        className="px-4 py-2 bg-dark/50 hover:bg-dark text-lightText rounded-lg transition-colors"
                                    >
                                        Close
                                    </button>

                                    <a
                                        href="#"
                                        className="px-4 py-2 bg-primary hover:bg-primary/80 text-white rounded-lg transition-colors"
                                    >
                                        Share Vision
                                    </a>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </Layout>
    );
};

export default FutureVisions; 