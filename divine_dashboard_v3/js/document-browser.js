/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * Divine Book Browser
 * Document browser functionality for Divine Dashboard v3
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize document browser functionality
    initDocumentBrowser();
});

// Global document database
let documentDatabase = [];
let currentDocument = null;

/**
 * Initialize document browser
 */
function initDocumentBrowser() {
    // Initialize markdown renderer
    initMarkdownRenderer();

    // Fetch documents
    fetchDocuments();

    // Set up event listeners
    setupDocumentBrowserEvents();
}

/**
 * Initialize Markdown renderer with Highlight.js
 */
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

/**
 * Fetch document list from API
 */
async function fetchDocuments() {
    try {
        const response = await fetch('/api/documents');
        if (response.ok) {
            documentDatabase = await response.json();
        } else {
            throw new Error('Failed to fetch documents');
        }
    } catch (error) {
        console.error('Error fetching documents:', error);
        // Fallback to simulated data
        documentDatabase = getSimulatedDocuments();
    }

    // Display all documents by default
    displayDocuments('all');
}

/**
 * Get simulated document data (fallback if API fails)
 */
function getSimulatedDocuments() {
    return [
        {
            path: 'BOOK/README.md',
            title: 'README',
            category: 'DOCUMENTATION',
            description: 'Main documentation for OMEGA BTC AI',
            type: 'md'
        },
        {
            path: 'BOOK/QUANTUM_PORTFOLIO_OPTIMIZER.md',
            title: 'Quantum Portfolio Optimizer',
            category: 'QUANTUM',
            description: 'Quantum computing approach to portfolio optimization',
            type: 'md'
        },
        {
            path: 'BOOK/README.html',
            title: 'README',
            category: 'DOCUMENTATION',
            description: 'HTML version of main documentation',
            type: 'html'
        },
        {
            path: 'BOOK/QUANTUM_PORTFOLIO_OPTIMIZER.html',
            title: 'Quantum Portfolio Optimizer',
            category: 'QUANTUM',
            description: 'HTML version of quantum portfolio optimizer',
            type: 'html'
        },
        {
            path: 'BOOK/SACRED_PATTERNS.md',
            title: 'Sacred Patterns',
            category: 'DIVINE',
            description: 'Sacred mathematical patterns for market analysis',
            type: 'md'
        },
        {
            path: 'BOOK/SACRED_PATTERNS.html',
            title: 'Sacred Patterns',
            category: 'DIVINE',
            description: 'HTML version of sacred patterns document',
            type: 'html'
        },
        {
            path: 'BOOK/divine_chronicles/COSMIC_MARKET_HARMONY_RESTORATION.md',
            title: 'Cosmic Market Harmony Restoration',
            category: 'COSMIC',
            description: 'Restoration of cosmic market harmony',
            type: 'md'
        },
        {
            path: 'BOOK/divine_chronicles/SACRED_FIBONACCI_MANUSCRIPT.md',
            title: 'Sacred Fibonacci Manuscript',
            category: 'DIVINE',
            description: 'The divine proportions revealed through sacred geometry',
            type: 'md'
        },
        {
            path: 'BOOK/divine_chronicles/TRINITY_BRINKS_MATRIX.md',
            title: 'Trinity Brinks Matrix',
            category: 'TRADING',
            description: 'The trinity of market forces in the Brinks matrix',
            type: 'md'
        }
    ];
}

/**
 * Display documents filtered by category
 */
function displayDocuments(category) {
    const documentList = document.getElementById('document-list');

    // Update category title
    const categoryTitle = document.getElementById('category-title');
    categoryTitle.textContent = category === 'all' ? 'All Documents' : `${category} Documents`;

    // Clear previous list
    documentList.innerHTML = '';

    // Filter documents
    let filteredDocs = documentDatabase;

    // Only show markdown versions in the list (HTML versions will be available in the viewer)
    filteredDocs = filteredDocs.filter(doc => doc.type === 'md');

    // Filter by category if not "all"
    if (category !== 'all') {
        filteredDocs = filteredDocs.filter(doc => doc.category === category);
    }

    // Display documents
    if (filteredDocs.length === 0) {
        documentList.innerHTML = '<div class="no-documents">No documents found</div>';
    } else {
        filteredDocs.forEach(doc => {
            const docItem = document.createElement('div');
            docItem.className = 'document-item';
            docItem.setAttribute('data-path', doc.path);

            // Find corresponding HTML file for this markdown file
            const htmlPath = doc.path.replace('.md', '.html');
            const hasHtmlVersion = documentDatabase.some(d => d.path === htmlPath);

            docItem.innerHTML = `
                <h4>${doc.title}</h4>
                <p>${doc.description || 'No description available'}</p>
                <span class="category-tag">${doc.category}</span>
            `;

            // Add click event to load document
            docItem.addEventListener('click', () => {
                // Remove active class from all items
                document.querySelectorAll('.document-item').forEach(item => {
                    item.classList.remove('active');
                });

                // Add active class to clicked item
                docItem.classList.add('active');

                // Load document
                loadDocument(doc.path, hasHtmlVersion ? htmlPath : null, doc.title);
            });

            documentList.appendChild(docItem);
        });
    }
}

/**
 * Load document content into viewer
 */
async function loadDocument(mdPath, htmlPath, title) {
    const markdownViewer = document.getElementById('markdown-viewer');
    const htmlViewer = document.getElementById('html-viewer');
    const documentTitle = document.getElementById('document-title');
    const openInBrowserBtn = document.getElementById('open-in-browser-btn');

    // Update document title
    documentTitle.textContent = title;

    // Show loading state
    markdownViewer.innerHTML = '<div class="loading-indicator">Loading document...</div>';
    htmlViewer.innerHTML = '';

    try {
        // Store current document info
        currentDocument = {
            mdPath: mdPath,
            htmlPath: htmlPath,
            title: title
        };

        // Fetch markdown content
        const mdResponse = await fetch(mdPath);
        if (mdResponse.ok) {
            const mdContent = await mdResponse.text();
            markdownViewer.innerHTML = marked.parse(mdContent);

            // Apply highlighting to code blocks
            markdownViewer.querySelectorAll('pre code').forEach(block => {
                hljs.highlightElement(block);
            });
        } else {
            markdownViewer.innerHTML = '<div class="error">Failed to load markdown document</div>';
        }

        // Fetch HTML content if available
        if (htmlPath) {
            try {
                const htmlResponse = await fetch(htmlPath);
                if (htmlResponse.ok) {
                    const htmlContent = await htmlResponse.text();

                    // Extract body content from HTML
                    const bodyMatch = htmlContent.match(/<body[^>]*>([\s\S]*)<\/body>/i);
                    const bodyContent = bodyMatch ? bodyMatch[1] : htmlContent;

                    htmlViewer.innerHTML = bodyContent;
                } else {
                    htmlViewer.innerHTML = '<div class="error">Failed to load HTML document</div>';
                }
            } catch (error) {
                htmlViewer.innerHTML = '<div class="error">Error loading HTML version</div>';
            }
        } else {
            htmlViewer.innerHTML = '<div class="error">No HTML version available</div>';
        }

        // Update open in browser button
        openInBrowserBtn.onclick = () => {
            window.open(mdPath, '_blank');
        };

    } catch (error) {
        console.error('Error loading document:', error);
        markdownViewer.innerHTML = '<div class="error">Error loading document</div>';
    }
}

/**
 * Set up event listeners for document browser
 */
function setupDocumentBrowserEvents() {
    // Category filters
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            // Remove active class from all filters
            categoryFilters.forEach(f => f.classList.remove('active'));

            // Add active class to clicked filter
            filter.classList.add('active');

            // Display documents for this category
            const category = filter.getAttribute('data-category');
            displayDocuments(category);
        });
    });

    // Toggle view button
    const toggleViewBtn = document.getElementById('toggle-view-btn');
    toggleViewBtn.addEventListener('click', () => {
        const markdownViewer = document.getElementById('markdown-viewer');
        const htmlViewer = document.getElementById('html-viewer');

        if (markdownViewer.classList.contains('active')) {
            markdownViewer.classList.remove('active');
            htmlViewer.classList.add('active');
            toggleViewBtn.innerHTML = '<i class="fas fa-code"></i> Show Markdown';
        } else {
            htmlViewer.classList.remove('active');
            markdownViewer.classList.add('active');
            toggleViewBtn.innerHTML = '<i class="fas fa-code"></i> Show HTML';
        }
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    function performSearch() {
        const query = searchInput.value.trim().toLowerCase();
        if (query === '') {
            // If empty query, show all documents
            displayDocuments('all');
            return;
        }

        // Filter documents by search query
        const results = documentDatabase.filter(doc =>
            doc.type === 'md' && (
                doc.title.toLowerCase().includes(query) ||
                doc.description.toLowerCase().includes(query) ||
                doc.category.toLowerCase().includes(query)
            )
        );

        // Display search results
        const documentList = document.getElementById('document-list');
        const categoryTitle = document.getElementById('category-title');

        categoryTitle.textContent = `Search Results for "${query}"`;
        documentList.innerHTML = '';

        if (results.length === 0) {
            documentList.innerHTML = '<div class="no-documents">No matching documents found</div>';
        } else {
            results.forEach(doc => {
                const docItem = document.createElement('div');
                docItem.className = 'document-item';
                docItem.setAttribute('data-path', doc.path);

                const htmlPath = doc.path.replace('.md', '.html');
                const hasHtmlVersion = documentDatabase.some(d => d.path === htmlPath);

                docItem.innerHTML = `
                    <h4>${doc.title}</h4>
                    <p>${doc.description || 'No description available'}</p>
                    <span class="category-tag">${doc.category}</span>
                `;

                docItem.addEventListener('click', () => {
                    document.querySelectorAll('.document-item').forEach(item => {
                        item.classList.remove('active');
                    });
                    docItem.classList.add('active');
                    loadDocument(doc.path, hasHtmlVersion ? htmlPath : null, doc.title);
                });

                documentList.appendChild(docItem);
            });
        }
    }

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
} 