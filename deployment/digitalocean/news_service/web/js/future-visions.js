// Future Visions Manager
document.addEventListener('DOMContentLoaded', function () {
    // Future visions data
    const futureVisions = [
        {
            id: 'vision-2030',
            title: 'Bitcoin in 2030',
            image: 'images/bitcoin_2030.png',
            description: 'By 2030, Bitcoin has evolved beyond mere currency. <span class="future-vision-highlight">nation-states hold significant BTC reserves</span>, and the Lightning Network facilitates billions of daily transactions.',
            quote: 'Bitcoin has redefined the concept of value storage and transfer in ways our ancestors with physical gold could never have imagined.',
            year: '2030',
            tags: ['adoption', 'lightning-network', 'reserve-currency']
        },
        {
            id: 'vision-quantum',
            title: 'Quantum Bitcoin',
            image: 'images/bitcoin_quantum.png',
            description: 'Quantum-resistant algorithms have been implemented to protect Bitcoin against the rise of quantum computing, ensuring the network\'s <span class="future-vision-highlight">cryptographic security</span> for generations to come.',
            quote: 'When classical cryptography faced its greatest threat, Bitcoin adapted and emerged stronger, just as its mysterious creator envisioned.',
            year: '2035',
            tags: ['quantum-resistance', 'security', 'evolution']
        }
    ];

    // Initialize the future visions section
    initFutureVisions();

    // Function to initialize future visions
    function initFutureVisions() {
        const futureVisionsContainer = document.getElementById('future-visions-container');

        if (!futureVisionsContainer) {
            console.error('Future visions container not found');
            return;
        }

        // Clear existing content
        futureVisionsContainer.innerHTML = '';

        // Add title section
        const titleSection = document.createElement('div');
        titleSection.className = 'future-visions-title mb-4';
        titleSection.innerHTML = `
            <h2 class="text-warning mb-3" data-i18n="Future Visions">Future Visions</h2>
            <p class="lead mb-0 text-light">OMEGA's algorithmic glimpses into Bitcoin's potential futures</p>
        `;
        futureVisionsContainer.appendChild(titleSection);

        // Add visions
        futureVisions.forEach(vision => {
            const visionCard = createVisionCard(vision);
            futureVisionsContainer.appendChild(visionCard);
        });
    }

    // Function to create a vision card
    function createVisionCard(vision) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card mb-5 golden-glow';
        cardDiv.id = vision.id;

        // Alternate layout direction for each card
        const isReversed = futureVisions.indexOf(vision) % 2 === 1;

        cardDiv.innerHTML = `
            <div class="card-body p-0">
                <div class="row g-0 ${isReversed ? 'flex-row-reverse' : ''}">
                    <div class="col-md-7">
                        <img src="${vision.image}" alt="${vision.title}" class="img-fluid rounded-start" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <div class="col-md-5 d-flex flex-column">
                        <div class="card-body h-100 d-flex flex-column justify-content-center">
                            <div class="d-flex align-items-center mb-2">
                                <h3 class="card-title text-warning mb-0" style="text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);">${vision.title}</h3>
                                <span class="ms-2 year-badge">${vision.year}</span>
                            </div>
                            <p class="card-text mb-4">${vision.description}</p>
                            <div class="divine-quote">
                                "${vision.quote}"
                            </div>
                            <div class="mt-auto pt-3">
                                ${vision.tags.map(tag => `<span class="badge ${tag.toLowerCase().includes('vision') ? 'bg-warning text-dark' : 'bg-dark'} me-2">${tag}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return cardDiv;
    }

    // Add a style for the year badge
    const style = document.createElement('style');
    style.textContent = `
        .year-badge {
            background-color: rgba(247, 147, 26, 0.2);
            color: #f7931a;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            border: 1px solid rgba(247, 147, 26, 0.4);
        }
        
        .divine-quote {
            border-left: 3px solid #f7931a;
            padding-left: 15px;
            font-style: italic;
            margin-bottom: 20px;
            color: #e0e0e0;
        }
    `;
    document.head.appendChild(style);
}); 