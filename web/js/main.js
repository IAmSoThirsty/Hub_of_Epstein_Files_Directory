// Main JavaScript for Epstein Files Codex

// Search functionality
function performSearch() {
    const query = document.getElementById('main-search').value;
    if (!query || query.trim() === '') {
        alert('Please enter a search query');
        return;
    }
    
    // Show results section
    document.getElementById('search-results').style.display = 'block';
    
    // Simulate search (in production, this would call backend API)
    searchDocuments(query);
}

function searchDocuments(query) {
    // This would integrate with backend search API
    console.log('Searching for:', query);
    
    // Update results count
    document.getElementById('results-count').innerHTML = 
        `Found <strong>147</strong> results for "${query}"`;
    
    // Display sample results
    displayResults([
        {
            id: 'doc-001',
            title: 'Court Filing - SDNY Case 19-cr-490',
            date: '2019-07-08',
            category: 'Legal',
            excerpt: 'Indictment of Jeffrey Epstein...',
            source: 'SDNY',
            verification: 1
        }
        // More results...
    ]);
}

function displayResults(results) {
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    
    results.forEach(result => {
        const resultCard = document.createElement('div');
        resultCard.className = 'result-card';
        resultCard.innerHTML = `
            <h3>${result.title}</h3>
            <div class="result-meta">
                <span>📅 ${result.date}</span>
                <span>📂 ${result.category}</span>
                <span>✅ Level ${result.verification}</span>
            </div>
            <p>${result.excerpt}</p>
            <button class="btn btn-sm btn-primary" onclick="viewDocument('${result.id}')">View Document</button>
        `;
        container.appendChild(resultCard);
    });
}

function toggleAdvanced() {
    const panel = document.getElementById('advanced-filters');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function applyFilters() {
    // Collect all filter values
    const filters = {
        dateFrom: document.getElementById('filter-date-from').value,
        dateTo: document.getElementById('filter-date-to').value,
        location: Array.from(document.getElementById('filter-location').selectedOptions).map(o => o.value),
        category: Array.from(document.getElementById('filter-category').selectedOptions).map(o => o.value),
        // ... more filters
    };
    
    console.log('Applied filters:', filters);
    performSearch();
}

function resetFilters() {
    document.querySelectorAll('#advanced-filters input, #advanced-filters select').forEach(input => {
        if (input.type === 'checkbox') {
            input.checked = input.id === 'filter-unredacted' || input.id === 'filter-partial-redacted';
        } else {
            input.value = '';
        }
    });
}

function setSearch(query) {
    document.getElementById('main-search').value = query;
    performSearch();
}

function setDateRange(period) {
    const ranges = {
        '1990-2000': ['1990-01-01', '2000-12-31'],
        '2000-2008': ['2000-01-01', '2008-12-31'],
        '2008-2015': ['2008-01-01', '2015-12-31'],
        '2015-2019': ['2015-01-01', '2019-12-31'],
        '2019-2020': ['2019-01-01', '2020-12-31'],
        '2020-2024': ['2020-01-01', '2024-12-31']
    };
    
    if (ranges[period]) {
        document.getElementById('filter-date-from').value = ranges[period][0];
        document.getElementById('filter-date-to').value = ranges[period][1];
    }
}

function loadPreset(presetId) {
    const presets = {
        'palm-beach-2005': {
            query: 'Palm Beach investigation',
            dateFrom: '2005-01-01',
            dateTo: '2008-12-31',
            location: ['palm-beach']
        },
        'flight-logs-all': {
            query: 'flight logs',
            category: ['flight-logs']
        },
        'maxwell-trial': {
            query: 'Maxwell trial',
            dateFrom: '2020-07-02',
            dateTo: '2022-06-28',
            category: ['legal']
        },
        'little-st-james': {
            query: 'Little St. James',
            location: ['little-st-james']
        },
        'unsealed-2023': {
            query: 'unsealed',
            dateFrom: '2023-01-01',
            sealedStatus: 'recently-unsealed'
        }
    };
    
    if (presets[presetId]) {
        const preset = presets[presetId];
        document.getElementById('main-search').value = preset.query || '';
        if (preset.dateFrom) document.getElementById('filter-date-from').value = preset.dateFrom;
        if (preset.dateTo) document.getElementById('filter-date-to').value = preset.dateTo;
        // Apply other filters...
        performSearch();
    }
}

function exportResults(format) {
    alert(`Exporting results as ${format.toUpperCase()}. Feature coming soon!`);
    // In production: generate and download file
}

function viewDocument(docId) {
    // In production: open document viewer
    alert(`Document ${docId} viewer will open here. Integration with document storage pending.`);
    // window.location.href = `codex.html#document-${docId}`;
}

function setView(viewType) {
    document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`view-${viewType}`).classList.add('active');
    // Update results display
}

// Codex browsing
function browseCategory(category) {
    window.location.href = `category.html?cat=${category}`;
}

function browsePeriod(period) {
    window.location.href = `timeline.html?period=${period}`;
}

function browseJurisdiction(jurisdiction) {
    window.location.href = `jurisdiction.html?j=${jurisdiction}`;
}

function viewCollection(collectionId) {
    window.location.href = `collection.html?id=${collectionId}`;
}

// Slideshow functions
function startSlideshow(slideshowId) {
    window.location.href = `slideshow-viewer.html?id=${slideshowId}`;
}

function downloadSlideshow(slideshowId) {
    alert('Downloading slideshow. Feature coming soon!');
}

// Infographic functions
function viewInfographic(infoId) {
    window.location.href = `infographic-viewer.html?id=${infoId}`;
}

function downloadInfographic(infoId) {
    alert('Downloading infographic. Feature coming soon!');
}

// Characters page filtering
if (document.getElementById('character-search')) {
    document.getElementById('character-search').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        document.querySelectorAll('.character-card').forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(searchTerm) ? 'block' : 'none';
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Epstein Files Codex initialized');
    
    // Add enter key support for search
    const searchInput = document.getElementById('main-search');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    // Scroll progress indicator
    const scrollProgress = document.querySelector('.scroll-progress');
    if (scrollProgress) {
        window.addEventListener('scroll', function() {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = window.scrollY;
            const progress = (scrolled / documentHeight) * 100;
            scrollProgress.style.width = progress + '%';
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Parallax effect on scroll
    window.addEventListener('scroll', function() {
        const scrolled = window.scrollY;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
            hero.style.opacity = 1 - (scrolled / 600);
        }
    });
    
    // Add cursor trail effect
    let cursorTrails = [];
    const maxTrails = 8;
    
    document.addEventListener('mousemove', function(e) {
        // Create cursor trail element
        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        trail.style.left = e.clientX + 'px';
        trail.style.top = e.clientY + 'px';
        document.body.appendChild(trail);
        
        cursorTrails.push(trail);
        
        // Remove old trails
        if (cursorTrails.length > maxTrails) {
            const oldTrail = cursorTrails.shift();
            oldTrail.remove();
        }
        
        // Auto remove after animation
        setTimeout(() => {
            trail.style.opacity = '0';
            setTimeout(() => trail.remove(), 500);
        }, 500);
    });
    
    // Enhanced stat counter animation
    const stats = document.querySelectorAll('.stat-number');
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const text = target.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                
                if (!isNaN(number)) {
                    animateValue(target, 0, number, 2000, text);
                }
                statsObserver.unobserve(target);
            }
        });
    }, observerOptions);
    
    stats.forEach(stat => statsObserver.observe(stat));
    
    function animateValue(element, start, end, duration, originalText) {
        const startTime = performance.now();
        const suffix = originalText.replace(/[\d,]/g, '');
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(progress * (end - start) + start);
            
            element.textContent = current.toLocaleString() + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }
});

// Save search preset
function saveSearchPreset() {
    const presetName = prompt('Enter a name for this search preset:');
    if (presetName) {
        // Save to localStorage or backend
        const preset = {
            name: presetName,
            query: document.getElementById('main-search').value,
            filters: {}
            // Collect all filter values
        };
        localStorage.setItem(`preset_${Date.now()}`, JSON.stringify(preset));
        alert('Search preset saved!');
    }
}

// PDF upload validation
function validatePDFUpload(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        alert('Only PDF files are accepted');
        return false;
    }
    
    if (file.size > 100 * 1024 * 1024) { // 100MB
        alert('File size must be under 100MB');
        return false;
    }
    
    return true;
}

function uploadPDF() {
    const fileInput = document.getElementById('pdf-upload');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    if (!validatePDFUpload(file)) {
        return;
    }
    
    // Show upload progress
    document.getElementById('upload-status').style.display = 'block';
    document.getElementById('upload-status').textContent = 'Uploading and analyzing...';
    
    // In production: upload to server
    setTimeout(() => {
        document.getElementById('upload-status').textContent = 'Analysis complete! File will be indexed if relevant.';
    }, 3000);
}
