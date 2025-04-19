import { ReactNode } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

interface LayoutProps {
    children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <div className="flex h-screen overflow-hidden bg-darkBg text-light">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="flex flex-col flex-1 overflow-hidden">
                {/* Navbar */}
                <Navbar />

                {/* Content Area with Scrolling */}
                <main className="flex-1 overflow-y-auto p-6">
                    {children}
                </main>

                {/* Footer */}
                <footer className="py-4 px-6 bg-secondary text-xs text-center opacity-70">
                    <div>
                        OMEGA BTC AI Platform © {new Date().getFullYear()} | May fortune favor the bold
                    </div>
                </footer>
            </div>
        </div>
    );
};

export default Layout; 