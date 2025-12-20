// Search functionality for Epstein Files Codex

// Toggle advanced filters
function toggleAdvanced() {
    const advancedFilters = document.getElementById('advancedFilters');
    const toggleText = document.getElementById('toggleText');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (advancedFilters.style.display === 'none' || !advancedFilters.style.display) {
        advancedFilters.style.display = 'block';
        toggleText.textContent = 'Hide Advanced Filters';
        toggleIcon.textContent = '▲';
    } else {
        advancedFilters.style.display = 'none';
        toggleText.textContent = 'Show Advanced Filters';
        toggleIcon.textContent = '▼';
    }
}

// Reset search form
function resetSearch() {
    document.getElementById('searchForm').reset();
    document.getElementById('resultsContainer').style.display = 'none';
}

// Handle form submission
document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    performSearch();
});

// Perform search (connects to backend API in production)
function performSearch() {
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsList = document.getElementById('resultsList');
    const resultsCount = document.getElementById('resultsCount');

    // Show loading state
    resultsContainer.style.display = 'block';
    resultsList.innerHTML = '<div class="loading-state">Searching files...</div>';

    // Collect form data
    const formData = {
        keyword: document.getElementById('keyword').value,
        documentType: document.getElementById('documentType').value,
        dateFrom: document.getElementById('dateFrom').value,
        dateTo: document.getElementById('dateTo').value,
        location: document.getElementById('location').value,
        locationKeyword: document.getElementById('locationKeyword').value,
        redactionStatus: getSelectedCheckboxes('redaction'),
        person: document.getElementById('person')?.value,
        caseNumber: document.getElementById('caseNumber')?.value,
        fileSource: document.getElementById('fileSource')?.value,
        relevanceScore: document.getElementById('relevanceScore')?.value,
        contentFlags: getSelectedCheckboxes('contentFlags')
    };

    // In production, this would call the backend API
    // For now, use mock data
    setTimeout(() => {
        const mockResults = generateMockResults(formData);
        displayResults(mockResults);
        resultsCount.textContent = `${mockResults.length} Result${mockResults.length !== 1 ? 's' : ''} Found`;
    }, 1500);
}

// Get selected checkbox values
function getSelectedCheckboxes(name) {
    const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    return Array.from(checkboxes).map(cb => cb.value);
}

// Generate mock search results
function generateMockResults(formData) {
    const keyword = formData.keyword?.toLowerCase() || '';
    
    // If no search criteria, return empty
    if (!keyword && !formData.dateFrom && !formData.location && !formData.person) {
        return [];
    }

    // Mock results database
    const allResults = [
        {
            id: 1,
            title: 'Flight Log Entry - December 1999',
            type: 'Flight Log',
            date: '1999-12-15',
            location: 'Little St. James Island',
            redaction: 'Partially Redacted',
            snippet: 'Flight manifest showing passengers traveling to Little St. James Island. Multiple redacted names present in passenger list. This document was obtained through FOIA requests and contains critical travel information.',
            tags: ['Travel', 'Island', 'Witnesses', 'FOIA'],
            relevance: 95,
            source: 'Court Documents',
            caseNumber: 'CV-2015-1234'
        },
        {
            id: 2,
            title: 'Property Deed - Manhattan Townhouse',
            type: 'Property Record',
            date: '1998-08-20',
            location: 'Manhattan Townhouse (71st St)',
            redaction: 'Unredacted',
            snippet: 'Complete property transfer documentation for the Manhattan townhouse located at East 71st Street. Includes financial details, ownership structure, and transaction history.',
            tags: ['Property', 'Real Estate', 'New York', 'Financial'],
            relevance: 88,
            source: 'Government Records',
            caseNumber: null
        },
        {
            id: 3,
            title: 'Court Filing - Victim Testimony Excerpt',
            type: 'Court Filing',
            date: '2015-03-10',
            location: 'Palm Beach Estate',
            redaction: 'Redacted',
            snippet: 'Testimony regarding incidents at the Palm Beach estate. Multiple names and identifying details redacted per court order. Contains allegations of criminal activity and witness statements.',
            tags: ['Testimony', 'Legal', 'Evidence', 'Victim'],
            relevance: 92,
            source: 'Court Documents',
            caseNumber: 'CV-2015-5678'
        },
        {
            id: 4,
            title: 'Email Correspondence - Foundation Business',
            type: 'Email',
            date: '2010-06-22',
            location: 'New York',
            redaction: 'Partially Redacted',
            snippet: 'Email chain discussing foundation operations and scheduling. Some recipient names redacted. Discusses travel arrangements and business meetings.',
            tags: ['Communication', 'Foundation', 'Business', 'Correspondence'],
            relevance: 75,
            source: 'Media Leaks',
            caseNumber: null
        },
        {
            id: 5,
            title: 'Photographic Evidence - Island Facility',
            type: 'Photo',
            date: '2008-07-14',
            location: 'Little St. James Island',
            redaction: 'Unredacted',
            snippet: 'Aerial and ground-level photographs of structures and facilities on Little St. James Island. Shows property layout, buildings, and infrastructure. High-resolution images available.',
            tags: ['Photos', 'Evidence', 'Property', 'Island'],
            relevance: 85,
            source: 'Law Enforcement',
            caseNumber: 'INV-2019-9876'
        },
        {
            id: 6,
            title: 'Financial Transaction Records - 2005-2008',
            type: 'Financial Record',
            date: '2007-03-15',
            location: 'New York',
            redaction: 'Partially Redacted',
            snippet: 'Banking records showing wire transfers and financial transactions. Some account numbers and recipient names redacted. Covers period of 2005-2008.',
            tags: ['Financial', 'Banking', 'Transactions', 'Records'],
            relevance: 82,
            source: 'Government Records',
            caseNumber: 'FIN-2019-4321'
        },
        {
            id: 7,
            title: 'Deposition Transcript - Associate Testimony',
            type: 'Deposition',
            date: '2016-04-18',
            location: 'Florida',
            redaction: 'Redacted',
            snippet: 'Full deposition transcript from associate witness. Key names and sensitive details redacted per protective order. Contains information about business operations and travel.',
            tags: ['Deposition', 'Witness', 'Legal', 'Testimony'],
            relevance: 90,
            source: 'Court Documents',
            caseNumber: 'CV-2016-7890'
        },
        {
            id: 8,
            title: 'Property Inspection Report - New Mexico Ranch',
            type: 'Property Record',
            date: '2019-08-25',
            location: 'New Mexico Ranch (Zorro Ranch)',
            redaction: 'Unredacted',
            snippet: 'Law enforcement inspection report of the New Mexico property (Zorro Ranch). Details property features, structures, and items seized during investigation.',
            tags: ['Property', 'Investigation', 'Law Enforcement', 'Evidence'],
            relevance: 87,
            source: 'Law Enforcement',
            caseNumber: 'INV-2019-5555'
        }
    ];

    // Filter results based on search criteria
    return allResults.filter(result => {
        // Keyword search
        if (keyword) {
            const searchableText = `${result.title} ${result.snippet} ${result.tags.join(' ')}`.toLowerCase();
            if (!searchableText.includes(keyword)) return false;
        }

        // Document type filter
        if (formData.documentType && result.type.toLowerCase().replace(' ', '-') !== formData.documentType) {
            return false;
        }

        // Date range filter
        if (formData.dateFrom && result.date < formData.dateFrom) return false;
        if (formData.dateTo && result.date > formData.dateTo) return false;

        // Location filter
        if (formData.location && !result.location.toLowerCase().includes(formData.location.replace('-', ' '))) {
            return false;
        }

        // Location keyword
        if (formData.locationKeyword && !result.location.toLowerCase().includes(formData.locationKeyword.toLowerCase())) {
            return false;
        }

        // Redaction status filter
        if (formData.redactionStatus.length > 0) {
            const redactionMatch = formData.redactionStatus.some(status => {
                if (status === 'unredacted') return result.redaction === 'Unredacted';
                if (status === 'redacted') return result.redaction === 'Redacted';
                if (status === 'partially-redacted') return result.redaction === 'Partially Redacted';
                if (status === 'sealed') return result.redaction === 'Sealed';
                return false;
            });
            if (!redactionMatch) return false;
        }

        // Person filter
        if (formData.person && !result.snippet.toLowerCase().includes(formData.person.toLowerCase())) {
            return false;
        }

        // Case number filter
        if (formData.caseNumber && (!result.caseNumber || !result.caseNumber.includes(formData.caseNumber))) {
            return false;
        }

        // File source filter
        if (formData.fileSource && result.source.toLowerCase().replace(' ', '-') !== formData.fileSource) {
            return false;
        }

        // Relevance score filter
        if (formData.relevanceScore && result.relevance < parseInt(formData.relevanceScore)) {
            return false;
        }

        return true;
    });
}

// Display search results
function displayResults(results) {
    const resultsList = document.getElementById('resultsList');
    
    if (results.length === 0) {
        resultsList.innerHTML = `
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try adjusting your search filters or using different keywords.</p>
            </div>
        `;
        return;
    }

    const resultsHTML = results.map(result => `
        <article class="result-card">
            <div class="result-header">
                <h3 class="result-title">${result.title}</h3>
                <span class="result-type-badge">${result.type}</span>
            </div>
            <div class="result-meta">
                <span class="meta-item">
                    <strong>📅 Date:</strong> ${formatDate(result.date)}
                </span>
                <span class="meta-item">
                    <strong>📍 Location:</strong> ${result.location}
                </span>
                <span class="meta-item">
                    <strong>🔒 Status:</strong> ${result.redaction}
                </span>
                <span class="meta-item">
                    <strong>⭐ Relevance:</strong> ${result.relevance}%
                </span>
            </div>
            ${result.caseNumber ? `<div class="result-case"><strong>Case Number:</strong> ${result.caseNumber}</div>` : ''}
            <p class="result-snippet">${highlightKeywords(result.snippet)}</p>
            <div class="result-tags">
                ${result.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <div class="result-actions">
                <button class="btn btn-sm btn-primary" onclick="viewDocument(${result.id})">View Document</button>
                <button class="btn btn-sm btn-secondary" onclick="addToCollection(${result.id})">Add to Collection</button>
            </div>
        </article>
    `).join('');
    
    resultsList.innerHTML = resultsHTML;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

// Highlight search keywords in results
function highlightKeywords(text) {
    const keyword = document.getElementById('keyword').value;
    if (!keyword) return text;
    
    const regex = new RegExp(`(${keyword})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Sort results
function sortResults() {
    const sortBy = document.getElementById('sortBy').value;
    console.log('Sorting by:', sortBy);
    // In production, this would re-sort the actual results
    // For now, just trigger a new search
    performSearch();
}

// View document (placeholder)
function viewDocument(id) {
    alert(`Viewing document ${id}. In production, this would open the document viewer.`);
}

// Add to collection (placeholder)
function addToCollection(id) {
    alert(`Added document ${id} to your collection. In production, this would save to your research collection.`);
}

// Set search from example
function setSearch(query) {
    document.getElementById('keyword').value = query;
    performSearch();
}

// Update last updated timestamp
document.addEventListener('DOMContentLoaded', function() {
    const lastUpdatedEl = document.getElementById('lastUpdated');
    if (lastUpdatedEl) {
        lastUpdatedEl.textContent = new Date().toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }
});
