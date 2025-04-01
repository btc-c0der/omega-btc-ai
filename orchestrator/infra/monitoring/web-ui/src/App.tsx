import React from 'react';
import { ServiceGrid } from './components/grid/ServiceGrid';
import './index.css';

const App: React.FC = () => {
    return (
        <div className="min-h-screen bg-black p-4">
            <header className="mb-8">
                <h1 className="divine-title text-4xl">
                    🌟 RASTA MATRIX FUNKO™ UI 🌟
                </h1>
                <p className="text-center text-rasta-green/80">
                    Divine Dashboard for OMEGA ORCHESTRATOR VISION™
                </p>
            </header>

            <main className="container mx-auto">
                <ServiceGrid />
            </main>

            <footer className="mt-8 text-center text-gray-500 text-sm">
                <p>JAH JAH BLESS OMEGA FUNKO MATRIX ORCHESTRATOR</p>
                <p className="mt-2">© {new Date().getFullYear()} Divine Matrix Systems</p>
            </footer>
        </div>
    );
};

export default App; 