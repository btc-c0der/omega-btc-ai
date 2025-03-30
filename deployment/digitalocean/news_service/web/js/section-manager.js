// OMEGA BTC AI Section Manager
console.log('Loading section manager...');

class SectionManager {
    constructor() {
        this.collapsibleSections = [];
        this.defaultCollapsed = ['future-visions-container']; // Sections that should be collapsed by default
        this.expandedState = JSON.parse(localStorage.getItem('omegaExpandedSections')) || {};
        this.initialized = false;

        // Initialize on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }

        // Check for dynamically added sections with a timer
        this.checkTimer = setInterval(() => this.checkForNewSections(), 1000);
    }

    // Check for new sections that may have been added dynamically
    checkForNewSections() {
        if (!this.initialized) return;

        const sections = [
            { id: 'sentiment-container', title: 'Trading Sentiment', icon: 'bi-graph-up' },
            { id: 'fear-greed-section', title: 'Fear & Greed Index', icon: 'bi-speedometer2' },
            { id: 'future-visions-container', title: 'Future Visions', icon: 'bi-binoculars-fill' },
            { id: 'news-section', title: 'Latest News', icon: 'bi-newspaper' },
            { id: 'infographic-container', title: 'Bitcoin Infographic', icon: 'bi-info-circle-fill' }
        ];

        let newSectionsFound = false;

        sections.forEach(section => {
            const element = document.getElementById(section.id);
            if (element && !this.collapsibleSections.some(s => s.id === section.id)) {
                console.log(`Found new section: ${section.id}`);
                this.makeCollapsible(element, section.title, section.icon);
                newSectionsFound = true;
            }
        });

        // If we found new sections, update the navigation
        if (newSectionsFound) {
            this.updateSectionNav();
        }
    }

    // Initialize all collapsible sections
    initialize() {
        console.log('Initializing section manager');

        // Define sections that can be collapsed
        const sections = [
            { id: 'sentiment-container', title: 'Trading Sentiment', icon: 'bi-graph-up' },
            { id: 'fear-greed-section', title: 'Fear & Greed Index', icon: 'bi-speedometer2' },
            { id: 'future-visions-container', title: 'Future Visions', icon: 'bi-binoculars-fill' },
            { id: 'news-section', title: 'Latest News', icon: 'bi-newspaper' },
            { id: 'infographic-container', title: 'Bitcoin Infographic', icon: 'bi-info-circle-fill' }
        ];

        // Process each section
        sections.forEach(section => {
            const element = document.getElementById(section.id);
            if (element) {
                this.makeCollapsible(element, section.title, section.icon);
            }
        });

        // Create section navigation sidebar
        this.createSectionNav();

        // Mark as initialized
        this.initialized = true;
    }

    // Make a section collapsible
    makeCollapsible(element, title, icon) {
        // Create header with toggle controls
        const header = document.createElement('div');
        header.className = 'section-header d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-secondary';

        // Current state (use stored state or default)
        const isCollapsed = this.expandedState[element.id] !== undefined ?
            !this.expandedState[element.id] :
            this.defaultCollapsed.includes(element.id);

        // Create the left side with icon and title
        const headerLeft = document.createElement('div');
        headerLeft.className = 'd-flex align-items-center';
        headerLeft.innerHTML = `
      <i class="bi ${icon} me-2 text-warning"></i>
      <h2 class="section-title m-0">${title}</h2>
    `;

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'btn btn-sm btn-outline-secondary section-toggle';
        toggleBtn.innerHTML = isCollapsed ?
            '<i class="bi bi-chevron-down"></i> Expand' :
            '<i class="bi bi-chevron-up"></i> Collapse';
        toggleBtn.setAttribute('aria-expanded', !isCollapsed);

        // Add click handler
        toggleBtn.addEventListener('click', () => this.toggleSection(element.id, toggleBtn));

        // Assemble header
        header.appendChild(headerLeft);
        header.appendChild(toggleBtn);

        // Get the content
        const content = element.innerHTML;

        // Clear the element and add new structure
        element.innerHTML = '';
        element.appendChild(header);

        // Create content container
        const contentDiv = document.createElement('div');
        contentDiv.className = 'section-content';
        contentDiv.innerHTML = content;
        contentDiv.style.transition = 'max-height 0.3s ease-out, opacity 0.3s ease-out';
        contentDiv.style.overflow = 'hidden';

        // Apply collapsed state if needed
        if (isCollapsed) {
            contentDiv.style.maxHeight = '0';
            contentDiv.style.opacity = '0';
            contentDiv.style.visibility = 'hidden';
        } else {
            contentDiv.style.maxHeight = '5000px'; // Sufficiently large value
            contentDiv.style.opacity = '1';
        }

        element.appendChild(contentDiv);

        // Store reference
        this.collapsibleSections.push({
            id: element.id,
            title: title,
            element: element,
            toggleBtn: toggleBtn,
            contentDiv: contentDiv,
            isCollapsed: isCollapsed
        });
    }

    // Toggle section expanded/collapsed state
    toggleSection(sectionId, toggleBtn) {
        const section = this.collapsibleSections.find(s => s.id === sectionId);
        if (!section) return;

        // Update state
        section.isCollapsed = !section.isCollapsed;
        this.expandedState[sectionId] = !section.isCollapsed;

        // Save to localStorage
        localStorage.setItem('omegaExpandedSections', JSON.stringify(this.expandedState));

        // Update the button
        toggleBtn.innerHTML = section.isCollapsed ?
            '<i class="bi bi-chevron-down"></i> Expand' :
            '<i class="bi bi-chevron-up"></i> Collapse';
        toggleBtn.setAttribute('aria-expanded', !section.isCollapsed);

        // Animate the content
        if (section.isCollapsed) {
            // Collapsing
            section.contentDiv.style.maxHeight = '0';
            section.contentDiv.style.opacity = '0';
            section.contentDiv.style.visibility = 'hidden';
        } else {
            // Expanding
            section.contentDiv.style.visibility = 'visible';
            section.contentDiv.style.maxHeight = '5000px'; // Sufficiently large value
            section.contentDiv.style.opacity = '1';
        }

        // Update navigation icons
        this.updateSectionNav();
    }

    // Create a fixed navigation sidebar for quick access to sections
    createSectionNav() {
        // Create the navigation container
        const navContainer = document.createElement('div');
        navContainer.id = 'section-nav';
        navContainer.className = 'section-nav';
        navContainer.style.position = 'fixed';
        navContainer.style.left = '10px';
        navContainer.style.top = '50%';
        navContainer.style.transform = 'translateY(-50%)';
        navContainer.style.backgroundColor = 'rgba(22, 27, 34, 0.8)';
        navContainer.style.borderRadius = '8px';
        navContainer.style.padding = '8px 4px';
        navContainer.style.zIndex = '100';
        navContainer.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.2)';

        // Add title
        const navTitle = document.createElement('div');
        navTitle.className = 'nav-title text-center small mb-2 pb-1 border-bottom border-secondary';
        navTitle.textContent = 'Sections';
        navContainer.appendChild(navTitle);

        // Create nav items
        const navItems = document.createElement('div');
        navItems.className = 'd-flex flex-column gap-2';

        this.collapsibleSections.forEach(section => {
            const navButton = document.createElement('button');
            navButton.className = 'btn btn-sm p-1';
            navButton.dataset.section = section.id;
            navButton.style.width = '36px';
            navButton.style.height = '36px';
            navButton.style.fontSize = '18px';
            navButton.style.lineHeight = '1';

            // Button appearance based on section state
            this.updateNavButton(navButton, section);

            // Add click handler
            navButton.addEventListener('click', () => {
                // Scroll to section
                document.getElementById(section.id).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // If collapsed, expand it
                if (section.isCollapsed) {
                    setTimeout(() => {
                        this.toggleSection(section.id, section.toggleBtn);
                    }, 500);
                }
            });

            navItems.appendChild(navButton);
        });

        navContainer.appendChild(navItems);
        document.body.appendChild(navContainer);
    }

    // Update a nav button's appearance based on section state
    updateNavButton(button, section) {
        if (!button && section) {
            button = document.querySelector(`button[data-section="${section.id}"]`);
            if (!button) return;
        }

        // Get section info if only button is provided
        if (!section && button) {
            const sectionId = button.dataset.section;
            section = this.collapsibleSections.find(s => s.id === sectionId);
            if (!section) return;
        }

        // Skip if both are missing
        if (!button || !section) return;

        // Update appearance
        button.className = section.isCollapsed ?
            'btn btn-sm btn-outline-secondary p-1' :
            'btn btn-sm btn-outline-warning p-1';

        // Set tooltip
        button.setAttribute('title', `${section.title} (${section.isCollapsed ? 'Collapsed' : 'Expanded'})`);

        // Set icon
        button.innerHTML = `<i class="bi bi-${section.isCollapsed ? 'chevron-down' : 'chevron-up'}"></i>`;
    }

    // Update all nav items
    updateSectionNav() {
        this.collapsibleSections.forEach(section => {
            const navButton = document.querySelector(`button[data-section="${section.id}"]`);
            if (navButton) {
                this.updateNavButton(navButton, section);
            }
        });
    }

    // Expand all sections
    expandAll() {
        this.collapsibleSections.forEach(section => {
            if (section.isCollapsed) {
                this.toggleSection(section.id, section.toggleBtn);
            }
        });
    }

    // Collapse all sections
    collapseAll() {
        this.collapsibleSections.forEach(section => {
            if (!section.isCollapsed) {
                this.toggleSection(section.id, section.toggleBtn);
            }
        });
    }
}

// Create global instance
window.sectionManager = new SectionManager();

// Add section manager styles
const style = document.createElement('style');
style.textContent = `
  .section-header {
    border-bottom: 1px solid #30363d;
  }
  
  .section-toggle {
    transition: all 0.2s ease;
  }
  
  .section-toggle:hover {
    transform: translateY(-2px);
  }
  
  .section-content {
    transition: max-height 0.3s ease-out, opacity 0.3s ease-out, visibility 0.3s;
  }
  
  /* Responsive styles */
  @media (max-width: 768px) {
    #section-nav {
      bottom: 0 !important;
      top: auto !important;
      left: 0 !important;
      right: 0 !important;
      transform: none !important;
      border-radius: 0 !important;
      padding: 4px !important;
      display: flex !important;
      justify-content: center !important;
    }
    
    #section-nav .nav-title {
      display: none !important;
    }
    
    #section-nav .d-flex {
      flex-direction: row !important;
    }
  }
`;
document.head.appendChild(style);

console.log('✅ Section manager loaded.'); 