import { lazy, Suspense } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { motion } from "framer-motion";

// Lazy loaded components
const Dashboard = lazy(() => import("./pages/Dashboard"));
const FutureVisions = lazy(() => import("./pages/FutureVisions"));
const BitcoinInfoGraphic = lazy(() => import("./pages/BitcoinInfoGraphic"));
const SettingsPage = lazy(() => import("./pages/Settings"));

// Import global layout components
import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";
import LoadingSpinner from "./components/ui/LoadingSpinner";

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-darkBg text-lightText">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Navbar />
          <main className="flex-1 p-4 md:p-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="container mx-auto"
            >
              <Suspense fallback={<LoadingSpinner />}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/future-visions" element={<FutureVisions />} />
                  <Route path="/infographic" element={<BitcoinInfoGraphic />} />
                  <Route path="/settings" element={<SettingsPage />} />
                </Routes>
              </Suspense>
            </motion.div>
          </main>
          <footer className="py-4 px-8 text-center text-sm opacity-75">
            OMEGA BTC AI © {new Date().getFullYear()} | <span className="text-primary">JAH BLESS</span>
          </footer>
        </div>
      </div>
    </Router>
  );
}

export default App;
