import { useState } from "react";
import { motion } from "framer-motion";
import { Link, useLocation } from "react-router-dom";

const Sidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const location = useLocation();

    const navItems = [
        { path: "/", icon: "📊", label: "Dashboard" },
        { path: "/future-visions", icon: "🔮", label: "Future Visions" },
        { path: "/infographic", icon: "📈", label: "BTC Infographic" },
        { path: "/settings", icon: "⚙️", label: "Settings" },
    ];

    const variants = {
        expanded: { width: "250px" },
        collapsed: { width: "70px" }
    };

    const isActive = (path: string) => {
        return location.pathname === path;
    };

    return (
        <motion.div
            className="h-screen bg-darkBg flex flex-col py-6 shadow-xl"
            initial="expanded"
            animate={isCollapsed ? "collapsed" : "expanded"}
            variants={variants}
            transition={{ duration: 0.3 }}
        >
            {/* Sidebar Header */}
            <div className="px-4 mb-8 flex justify-between items-center">
                {!isCollapsed && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex items-center gap-2"
                    >
                        <span className="text-primary font-bold">OMEGA</span>
                        <span className="text-sm font-light">Navigation</span>
                    </motion.div>
                )}

                <button
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    className="p-1 rounded hover:bg-primary/20 text-lg transition-colors"
                >
                    {isCollapsed ? "→" : "←"}
                </button>
            </div>

            {/* Navigation Links */}
            <div className="flex flex-col gap-2 px-3">
                {navItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive(item.path)
                            ? "bg-primary text-darkBg"
                            : "hover:bg-dark hover:text-primary"
                            }`}
                    >
                        <span className="text-xl">{item.icon}</span>
                        {!isCollapsed && (
                            <motion.span
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                {item.label}
                            </motion.span>
                        )}
                    </Link>
                ))}
            </div>

            {/* Blockchain Status */}
            <div className="mt-auto px-4">
                <div className="border-t border-dark pt-4">
                    <div className="flex items-center gap-2 mb-2">
                        <div className="h-2 w-2 rounded-full bg-success animate-pulse"></div>
                        {!isCollapsed && (
                            <motion.span
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="text-xs opacity-75"
                            >
                                Blockchain Synced
                            </motion.span>
                        )}
                    </div>

                    {!isCollapsed && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="text-xs opacity-75"
                        >
                            <div>Latest Block: #835021</div>
                            <div>Network: Mainnet</div>
                        </motion.div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default Sidebar; 