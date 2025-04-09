import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Error boundary for catching runtime errors
class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean, error: Error | null }> {
    constructor(props: { children: React.ReactNode }) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    padding: '20px',
                    backgroundColor: '#121212',
                    color: '#FFD700',
                    fontFamily: 'monospace',
                    border: '1px solid #FF3D00',
                    borderRadius: '4px',
                    margin: '20px'
                }}>
                    <h2>Something went wrong:</h2>
                    <pre style={{
                        backgroundColor: 'rgba(255,61,0,0.1)',
                        padding: '10px',
                        borderRadius: '4px',
                        overflow: 'auto',
                        maxHeight: '300px'
                    }}>
                        {this.state.error?.message || 'Unknown error'}
                    </pre>
                    <button
                        onClick={() => window.location.reload()}
                        style={{
                            backgroundColor: '#00B52D',
                            color: 'white',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            marginTop: '10px'
                        }}
                    >
                        Reload Dashboard
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <ErrorBoundary>
            <App />
        </ErrorBoundary>
    </React.StrictMode>,
) 