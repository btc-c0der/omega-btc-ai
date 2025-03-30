import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

const Navbar = () => {
    const [moonPhase, setMoonPhase] = useState("🌕"); // Default full moon
    const [currentTime, setCurrentTime] = useState("");

    // Calculate Divine Cycle (Moon Phase)
    useEffect(() => {
        // Simple moon phase calculation for demonstration
        const calculateMoonPhase = () => {
            const phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"];
            const date = new Date();
            const dayOfYear = Math.floor(
                (date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000
            );

            // Fibonacci day calculation (mod 8)
            const fiboDay = dayOfYear % 8;
            return phases[fiboDay];
        };

        setMoonPhase(calculateMoonPhase());

        // Update time every second
        const interval = setInterval(() => {
            const now = new Date();
            setCurrentTime(now.toLocaleTimeString());
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <motion.nav
            className="bg-secondary py-4 px-6 shadow-lg"
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Link to="/" className="flex items-center gap-2">
                        <span className="text-primary text-2xl font-bold">OMEGA</span>
                        <span className="text-xl font-light">BTC AI</span>
                    </Link>

                    <div className="hidden md:flex ml-8 space-x-4">
                        <Link to="/" className="hover:text-primary transition-colors">Dashboard</Link>
                        <Link to="/future-visions" className="hover:text-primary transition-colors">Future Visions</Link>
                        <Link to="/infographic" className="hover:text-primary transition-colors">Infographic</Link>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    {/* Divine Cycle Display */}
                    <motion.div
                        className="hidden md:flex items-center gap-2 bg-darkBg px-3 py-1 rounded-full"
                        whileHover={{ scale: 1.05 }}
                    >
                        <span className="text-xl">{moonPhase}</span>
                        <div className="text-xs opacity-75">
                            <div>Divine Cycle</div>
                            <div>{currentTime}</div>
                        </div>
                    </motion.div>

                    {/* Status Indicator */}
                    <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-success animate-pulse"></div>
                        <span className="text-xs opacity-75 hidden md:inline">Connected</span>
                    </div>

                    {/* Settings Link */}
                    <Link to="/settings">
                        <motion.div
                            whileHover={{ rotate: 90 }}
                            transition={{ duration: 0.2 }}
                            className="text-xl cursor-pointer"
                        >
                            ⚙️
                        </motion.div>
                    </Link>
                </div>
            </div>
        </motion.nav>
    );
};

export default Navbar; 