/**
 * OMEGA Divine Book Browser
 * Main JavaScript functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    initMobileNav();
    initMarkdownRenderer();
    initDocumentList();
    initEventListeners();
});

// Mobile Navigation
function initMobileNav() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('nav ul');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
}

// Initialize Markdown Renderer with Highlight.js
function initMarkdownRenderer() {
    // Configure marked.js
    marked.setOptions({
        highlight: function (code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value;
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });
}

// Root path for the repository
const repoRoot = '.';
const bookPath = './BOOK';
const organizedBookPath = './BOOK/BOOK_ORGANIZED_20250409_114306'; // Most recent organized folder
const srcPath = './src';

// In-memory document database
let documentDatabase = [];

// Fetch and display document list
function initDocumentList() {
    // Load documents from entire repository
    fetchRepositoryDocuments()
        .then(documents => {
            documentDatabase = documents;
            displayDocumentList('all');
        })
        .catch(error => {
            console.error('Error loading documents:', error);
            displayErrorMessage('Failed to load document list. Please try refreshing the page.');
        });
}

// Fetch documents recursively from the entire repository
async function fetchRepositoryDocuments() {
    try {
        // This is a simulation for demo - in a real app, you would make a server call
        // that recursively scans the repository directories

        // Load simulated repository structure - in this case we're gathering documents from:
        // 1. Main BOOK directory
        // 2. Organized BOOK directory
        // 3. Source code directories with documentation

        const documents = [
            ...simulateBookDirectory(),
            ...simulateOrganizedDirectory(),
            ...simulateSourceDirectory()
        ];

        return documents;
    } catch (error) {
        console.error('Error fetching repository documents:', error);
        return [];
    }
}

// Simulate document list from main BOOK directory
function simulateBookDirectory() {
    const documents = [
        {
            path: `${bookPath}/README.md`,
            title: 'README',
            category: 'DOCUMENTATION',
            description: 'Main documentation for OMEGA BTC AI',
            type: 'md'
        },
        {
            path: `${bookPath}/QUANTUM_PORTFOLIO_OPTIMIZER.md`,
            title: 'Quantum Portfolio Optimizer',
            category: 'QUANTUM',
            description: 'Quantum computing approach to portfolio optimization',
            type: 'md'
        },
        {
            path: `${bookPath}/QUANTUM_SECURITY_METRICS_SYSTEM.md`,
            title: 'Quantum Security Metrics System',
            category: 'QUANTUM',
            description: 'Security framework for quantum systems',
            type: 'md'
        },
        {
            path: `${bookPath}/Z1N3_QUANTUM_SACRED_PATTERN.md`,
            title: 'Z1N3 Quantum Sacred Pattern',
            category: 'QUANTUM',
            description: 'Quantum patterns for trading',
            type: 'md'
        },
        {
            path: `${bookPath}/SACRED_PATTERNS.md`,
            title: 'Sacred Patterns',
            category: 'DIVINE',
            description: 'Sacred mathematical patterns for market analysis',
            type: 'md'
        },
        {
            path: `${bookPath}/QUANTUM_TOOLKIT_MANUAL.md`,
            title: 'Quantum Toolkit Manual',
            category: 'DOCUMENTATION',
            description: 'Manual for the quantum toolkit',
            type: 'md'
        },
        {
            path: `${bookPath}/QUANTUM_MOONET_RITUAL.md`,
            title: 'Quantum Moonet Ritual',
            category: 'DIVINE',
            description: 'Ritual for quantum moonet synchronization',
            type: 'md'
        },
        {
            path: `${bookPath}/QUANTUM_CELEBRATION_SONNET.md`,
            title: 'Quantum Celebration Sonnet',
            category: 'DIVINE',
            description: 'Sonnet celebrating quantum achievements',
            type: 'md'
        },
        // Add more from the BOOK directory
        {
            path: `${bookPath}/QUANTUM_SONNET_INSTALLATION.md`,
            title: 'Quantum Sonnet Installation',
            category: 'TECHNICAL',
            description: 'Installation guide for Quantum Sonnet',
            type: 'md'
        },
        {
            path: `${bookPath}/DIVINE_ENV_LOADER.md`,
            title: 'Divine Environment Loader',
            category: 'TECHNICAL',
            description: 'Environment loader for divine services',
            type: 'md'
        },
        {
            path: `${bookPath}/VIRGIL_ABLOH_INVOCATION.md`,
            title: 'Virgil Abloh Invocation',
            category: 'DIVINE',
            description: 'Invocation ritual for divine inspiration',
            type: 'md'
        },
        {
            path: `${bookPath}/OMEGA_BOTS_BUNDLE_DIVINE_GENESIS.md`,
            title: 'OMEGA Bots Bundle Divine Genesis',
            category: 'BOTS',
            description: 'Genesis documentation for OMEGA bot bundle',
            type: 'md'
        },
        {
            path: `${bookPath}/AIXBT_REALTIME_PRICE_FEED.md`,
            title: 'AIXBT Realtime Price Feed',
            category: 'TRADING',
            description: 'Real-time cryptocurrency price feed',
            type: 'md'
        }
    ];

    // Add corresponding HTML versions
    const htmlDocuments = documents.map(doc => ({
        ...doc,
        path: doc.path.replace('.md', '.html'),
        type: 'html'
    }));

    return [...documents, ...htmlDocuments];
}

// Simulate document list from organized BOOK directory
function simulateOrganizedDirectory() {
    const categories = ['QUANTUM', 'DIVINE', 'COSMIC', 'TECHNICAL', 'TRADING', 'DOCUMENTATION'];
    const documents = [];

    // Sample documents for each category in the organized directory
    categories.forEach(category => {
        const categoryDocs = [
            {
                path: `${organizedBookPath}/${category}/README.md`,
                title: `${category} Overview`,
                category: category,
                description: `Overview of the ${category} section`,
                type: 'md'
            },
            {
                path: `${organizedBookPath}/${category}/IMPLEMENTATION.md`,
                title: `${category} Implementation`,
                category: category,
                description: `Implementation details for ${category} systems`,
                type: 'md'
            },
            {
                path: `${organizedBookPath}/${category}/ARCHITECTURE.md`,
                title: `${category} Architecture`,
                category: category,
                description: `Architecture of the ${category} systems`,
                type: 'md'
            }
        ];

        documents.push(...categoryDocs);
    });

    // Add corresponding HTML versions
    const htmlDocuments = documents.map(doc => ({
        ...doc,
        path: doc.path.replace('.md', '.html'),
        type: 'html'
    }));

    return [...documents, ...htmlDocuments];
}

// Simulate document list from source code directories
function simulateSourceDirectory() {
    return [
        // Quantum encoding documentation from src directory
        {
            path: `${srcPath}/omega_bot_farm/ai_model_aixbt/quantum_encoding/README.md`,
            title: 'Quantum Encoding',
            category: 'SOURCE',
            description: 'Documentation for quantum encoding modules',
            type: 'md'
        },
        {
            path: `${srcPath}/omega_bot_farm/ai_model_aixbt/quantum_encoding/ENTANGLEMENT_ENCODING.md`,
            title: 'Entanglement Encoding',
            category: 'SOURCE',
            description: 'Technical details of entanglement encoding',
            type: 'md'
        },
        {
            path: `${srcPath}/omega_bot_farm/ai_model_aixbt/quantum_encoding/BASIS_ENCODING.md`,
            title: 'Basis Encoding',
            category: 'SOURCE',
            description: 'Technical details of basis encoding',
            type: 'md'
        },

        // Add more source directories - these would be discovered recursively in a real app
        {
            path: `${srcPath}/README.md`,
            title: 'Source README',
            category: 'SOURCE',
            description: 'Overview of the source code structure',
            type: 'md'
        },
        {
            path: `${srcPath}/docs/API_DOCUMENTATION.md`,
            title: 'API Documentation',
            category: 'SOURCE',
            description: 'API documentation for backend services',
            type: 'md'
        },

        // Example testing docs
        {
            path: `${srcPath}/tests/README.md`,
            title: 'Test Suite Documentation',
            category: 'TESTING',
            description: 'Overview of the test suite',
            type: 'md'
        },

        // Example deployment docs
        {
            path: `${repoRoot}/deployment/README.md`,
            title: 'Deployment Documentation',
            category: 'DEPLOYMENT',
            description: 'Deployment instructions',
            type: 'md'
        }
    ];
}

// Display document list by category
function displayDocumentList(category) {
    const documentList = document.getElementById('document-list');
    const categoryTitle = document.getElementById('category-title');

    // Clear the current list
    documentList.innerHTML = '';

    // Update category title
    if (category === 'all') {
        categoryTitle.textContent = 'All Documents';
    } else {
        categoryTitle.textContent = `${category} Documents`;
    }

    // Filter documents by category and only show MD versions (not HTML duplicates)
    const filteredDocuments = documentDatabase.filter(doc =>
        (category === 'all' || doc.category === category) && doc.type === 'md'
    );

    // Sort documents by title
    filteredDocuments.sort((a, b) => a.title.localeCompare(b.title));

    // Add documents to the list
    filteredDocuments.forEach(doc => {
        const docItem = document.createElement('div');
        docItem.className = 'document-item';
        docItem.dataset.path = doc.path;
        docItem.dataset.htmlPath = doc.path.replace('.md', '.html');

        docItem.innerHTML = `
            <h4>${doc.title}</h4>
            <p>${doc.description}</p>
        `;

        docItem.addEventListener('click', () => {
            // Remove active class from all items
            document.querySelectorAll('.document-item').forEach(item => {
                item.classList.remove('active');
            });

            // Add active class to clicked item
            docItem.classList.add('active');

            // Load the document
            loadDocument(doc.path, doc.path.replace('.md', '.html'), doc.title);
        });

        documentList.appendChild(docItem);
    });

    // Show message if no documents found
    if (filteredDocuments.length === 0) {
        documentList.innerHTML = '<p class="no-docs">No documents found in this category.</p>';
    }
}

// Load and display document content
async function loadDocument(mdPath, htmlPath, title) {
    const markdownViewer = document.getElementById('markdown-viewer');
    const htmlViewer = document.getElementById('html-viewer');
    const documentTitle = document.getElementById('document-title');
    const openInBrowserBtn = document.getElementById('open-in-browser-btn');

    // Update document title
    documentTitle.textContent = title;

    // Update open in browser button
    openInBrowserBtn.onclick = () => {
        window.open(htmlPath, '_blank');
    };

    try {
        // In a real application, you would fetch the actual file content
        // For this demo, we'll use simulated content based on the file path
        const mdContent = await fetchSimulatedContent(mdPath);
        const htmlContent = await fetchSimulatedContent(htmlPath);

        // Render Markdown content
        markdownViewer.innerHTML = marked.parse(mdContent);

        // Set HTML content
        htmlViewer.innerHTML = htmlContent;

        // Show Markdown viewer by default
        markdownViewer.classList.add('active');
        htmlViewer.classList.remove('active');

    } catch (error) {
        console.error('Error loading document:', error);
        markdownViewer.innerHTML = '<p class="error">Error loading document. Please try again.</p>';
    }
}

// Fetch simulated content for demo purposes
async function fetchSimulatedContent(path) {
    // This would be an actual AJAX request in a real application
    // For demo, return different content based on file path

    // Extract filename from path
    const filename = path.split('/').pop();
    const category = path.includes('/') ? path.split('/').slice(-2)[0] : 'Unknown';

    // Simulate delay
    await new Promise(resolve => setTimeout(resolve, 300));

    if (path.includes('README.md')) {
        return `# OMEGA BTC AI Documentation\n\nWelcome to the OMEGA BTC AI documentation. This repository contains information about our quantum-enhanced trading system.\n\n## Core Components\n\n- Quantum Data Encoding\n- Divine Market Analysis\n- Fibonacci Position Sizing\n- Schumann Resonance Integration\n\n## Getting Started\n\nRefer to the installation guide for setup instructions.\n\n## Repository Structure\n\nThis repository contains multiple directories:\n\n- \`BOOK/\`: Divine manuscripts and documentation\n- \`src/\`: Source code for the OMEGA BTC AI system\n- \`deployment/\`: Deployment configuration and scripts\n- \`docs/\`: Additional documentation`;
    }

    if (path.includes('quantum_encoding')) {
        return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\n## Quantum Encoding Implementation\n\nThis document describes the quantum encoding techniques used in our system.\n\n### Implementation Details\n\nThe \`quantum_encoding\` module provides various encoding strategies for transforming classical data into quantum states.\n\n\`\`\`python\nfrom abc import ABC, abstractmethod\n\nclass BaseEncoder(ABC):\n    \"\"\"Base class for all quantum encoders.\"\"\"\n    \n    def __init__(self, n_qubits):\n        self.n_qubits = n_qubits\n    \n    @abstractmethod\n    def encode(self, data):\n        \"\"\"Encode classical data into quantum state.\"\"\"\n        pass\n    \n    @abstractmethod\n    def decode(self, quantum_state):\n        \"\"\"Decode quantum state back to classical data.\"\"\"\n        pass\n\`\`\`\n\n### Usage Example\n\n\`\`\`python\nfrom quantum_encoding import AmplitudeEncoder\n\n# Initialize encoder\nencoder = AmplitudeEncoder(n_qubits=5)\n\n# Encode market data\nquantum_state = encoder.encode(market_data)\n\n# Process using quantum algorithms\nresult = quantum_processor.process(quantum_state)\n\n# Decode results\nclassical_result = encoder.decode(result)\n\`\`\``;
    }

    if (path.includes('QUANTUM')) {
        return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\n## Quantum Implementation Details\n\nThis document describes the quantum implementation of our trading system.\n\n### Quantum Superposition\n\nWe utilize quantum superposition to evaluate multiple trading scenarios simultaneously.\n\n\`\`\`python\ndef quantum_superposition(market_data):\n    # Initialize quantum state\n    q_state = QuantumRegister(5)\n    circuit = QuantumCircuit(q_state)\n    \n    # Apply Hadamard gates to create superposition\n    for i in range(5):\n        circuit.h(i)\n    \n    # Encode market data\n    circuit = encode_market_data(circuit, market_data)\n    \n    return circuit\n\`\`\`\n\n### Quantum Entanglement\n\nOur system uses quantum entanglement to model correlations between different market variables.`;
    }

    if (path.includes('DIVINE')) {
        return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\n## Divine Principles\n\nThis document outlines the divine principles behind our trading approach.\n\n### Sacred Geometry in Markets\n\nWe recognize the presence of sacred geometry, particularly the Golden Ratio (φ), in market structures.\n\n\`\`\`javascript\nfunction calculateGoldenRatio(price) {\n    const phi = 1.618033988749895;\n    return {\n        extension: price * phi,\n        retracement: price / phi\n    };\n}\n\`\`\`\n\n### Divine Time Cycles\n\nMarkets operate in divine cycles that correspond to cosmic rhythms.`;
    }

    if (path.includes('COSMIC')) {
        return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\n## Cosmic Integration\n\nThis document describes how we integrate cosmic principles into our trading system.\n\n### Cosmic Price Oracle\n\nThe Cosmic Price Oracle uses planetary alignments to predict market movements.\n\n\`\`\`python\nclass CosmicPriceOracle:\n    def __init__(self):\n        self.planetary_data = PlanetaryDataSource()\n        self.market_data = MarketDataSource()\n    \n    def predict_next_move(self):\n        alignment = self.planetary_data.get_current_alignment()\n        historical_pattern = self.find_similar_pattern(alignment)\n        return self.project_outcome(historical_pattern)\n\`\`\`\n\n### Matrix Connection\n\nOur system maintains a connection to the cosmic matrix that underlies all market movements.`;
    }

    if (path.includes('TECHNICAL') || path.includes('API') || path.includes('deployment')) {
        return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\n## Technical Documentation\n\nThis document provides technical details for the ${category} component.\n\n### Architecture\n\n\`\`\`\n+----------------+         +----------------+         +----------------+\n|                |         |                |         |                |\n|  Data Sources  | ------> |  Processors    | ------> |  Output Layer  |\n|                |         |                |         |                |\n+----------------+         +----------------+         +----------------+\n\`\`\`\n\n### Configuration\n\nThe system is configured using environment variables:\n\n\`\`\`bash\n# Core Configuration\nOMEGA_ENV=production\nQUANTUM_LEVEL=9\nDIVINE_ALIGNMENT=true\n\n# API Configuration\nAPI_PORT=8888\nAPI_HOST=0.0.0.0\n\`\`\`\n\n### Implementation\n\n\`\`\`python\nclass ${filename.replace('.md', '').replace(/_/g, '')}:\n    def __init__(self, config):\n        self.config = config\n        self.logger = setup_logger()\n        \n    def initialize(self):\n        self.logger.info(\"Initializing system...\")\n        # Implementation details\n\`\`\``;
    }

    if (path.includes('.html')) {
        // For HTML content, return a simplified version
        const title = filename.replace('.html', '').replace(/_/g, ' ');
        return `<div class="medium-instructions">
            <strong>Medium Import Instructions:</strong>
            <p>This is the HTML version of the document, formatted for Medium.</p>
        </div>
        <h1>${title}</h1>
        <p>This is the HTML version of the document, which includes Medium-specific formatting.</p>
        <p>In the actual implementation, this would contain the full HTML content of the document.</p>`;
    }

    // Default content for other documents
    return `# ${filename.replace('.md', '').replace(/_/g, ' ')}\n\nThis is a placeholder content for ${filename}.\n\n## Features\n\n- Feature 1\n- Feature 2\n- Feature 3\n\n## Implementation\n\n\`\`\`python\ndef main():\n    print("Implementation details would appear here")\n\`\`\`\n\n## Further Reading\n\nSee related documents for more information.`;
}

// Display error message
function displayErrorMessage(message) {
    const documentList = document.getElementById('document-list');
    documentList.innerHTML = `<p class="error">${message}</p>`;
}

// Initialize event listeners
function initEventListeners() {
    // Category links
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const category = link.getAttribute('data-category');
            displayDocumentList(category);
        });
    });

    // All documents link
    const allDocsLink = document.querySelector('.all-docs-link');
    if (allDocsLink) {
        allDocsLink.addEventListener('click', (e) => {
            e.preventDefault();
            displayDocumentList('all');
        });
    }

    // Toggle view button
    const toggleViewBtn = document.getElementById('toggle-view-btn');
    if (toggleViewBtn) {
        toggleViewBtn.addEventListener('click', () => {
            const mdViewer = document.getElementById('markdown-viewer');
            const htmlViewer = document.getElementById('html-viewer');
            mdViewer.classList.toggle('active');
            htmlViewer.classList.toggle('active');

            // Update button text based on active viewer
            if (mdViewer.classList.contains('active')) {
                toggleViewBtn.innerHTML = '<i class="fas fa-code"></i> View HTML';
            } else {
                toggleViewBtn.innerHTML = '<i class="fas fa-markdown"></i> View Markdown';
            }
        });
    }

    // Search functionality
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    if (searchInput && searchButton) {
        searchButton.addEventListener('click', () => {
            performSearch(searchInput.value);
        });

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch(searchInput.value);
            }
        });
    }

    // Code Stats link (now points to external page)
    const codeStatsLink = document.getElementById('code-stats-link');
    if (codeStatsLink) {
        // This is already handled by the href and target="_blank" in HTML
        // No need for additional JavaScript for a simple link
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // ALT + T to toggle view
        if (e.altKey && e.key === 't') {
            const toggleViewBtn = document.getElementById('toggle-view-btn');
            if (toggleViewBtn) {
                toggleViewBtn.click();
            }
        }

        // ESC to clear search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('search-input');
            if (searchInput && searchInput.value) {
                searchInput.value = '';
                displayDocumentList('all');
            }
        }

        // CTRL/CMD + F to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            const searchInput = document.getElementById('search-input');
            if (searchInput && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        }
    });
}

// Perform search
function performSearch(query) {
    if (!query.trim()) {
        displayDocumentList('all');
        return;
    }

    query = query.toLowerCase();

    // Filter documents that match the search query
    const searchResults = documentDatabase.filter(doc =>
        (doc.title.toLowerCase().includes(query) ||
            doc.description.toLowerCase().includes(query) ||
            doc.path.toLowerCase().includes(query)) &&
        doc.type === 'md'
    );

    const documentList = document.getElementById('document-list');
    const categoryTitle = document.getElementById('category-title');

    // Clear the current list
    documentList.innerHTML = '';

    // Update category title
    categoryTitle.textContent = `Search Results: ${query}`;

    // Sort results by relevance (title matches first)
    searchResults.sort((a, b) => {
        const aInTitle = a.title.toLowerCase().includes(query);
        const bInTitle = b.title.toLowerCase().includes(query);

        if (aInTitle && !bInTitle) return -1;
        if (!aInTitle && bInTitle) return 1;
        return a.title.localeCompare(b.title);
    });

    // Add search results to the list
    searchResults.forEach(doc => {
        const docItem = document.createElement('div');
        docItem.className = 'document-item';
        docItem.dataset.path = doc.path;
        docItem.dataset.htmlPath = doc.path.replace('.md', '.html');

        docItem.innerHTML = `
            <h4>${doc.title}</h4>
            <p>${doc.description}</p>
            <p class="category-tag">${doc.category}</p>
            <p class="path-info">${doc.path}</p>
        `;

        docItem.addEventListener('click', () => {
            document.querySelectorAll('.document-item').forEach(item => {
                item.classList.remove('active');
            });
            docItem.classList.add('active');
            loadDocument(doc.path, doc.path.replace('.md', '.html'), doc.title);
        });

        documentList.appendChild(docItem);
    });

    // Show message if no results found
    if (searchResults.length === 0) {
        documentList.innerHTML = '<p class="no-docs">No documents found matching your search.</p>';
    }
}

function initCodeStats() {
    // ... Remove all the code related to code stats ...
} 