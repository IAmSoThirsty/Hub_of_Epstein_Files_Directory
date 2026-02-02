/**
 * Dynamic Location Loader
 * Loads all location profiles from the generated database
 */

document.addEventListener('DOMContentLoaded', function() {
    // Load location data
    fetch('data/locations_index.json')
        .then(response => response.json())
        .then(locations => {
            renderLocations(locations);
            setupLocationSearch(locations);
        })
        .catch(error => {
            console.error('Error loading locations:', error);
            // Try to load from the full database
            loadFromDatabase();
        });
});

function loadFromDatabase() {
    const locations = [
        {id: 'little_st_james', name: 'Little St. James Island', type: 'Private Island', country: 'U.S. Virgin Islands'},
        {id: 'great_st_james', name: 'Great St. James Island', type: 'Private Island', country: 'U.S. Virgin Islands'},
        {id: 'palm_beach', name: 'Palm Beach Residence', type: 'Private Residence', country: 'USA'},
        {id: 'new_york', name: 'Manhattan Townhouse', type: 'Private Residence', country: 'USA'},
        {id: 'paris', name: 'Paris Apartment', type: 'Private Residence', country: 'France'},
        {id: 'new_mexico', name: 'Zorro Ranch', type: 'Ranch', country: 'USA'},
        {id: 'mar_a_lago', name: 'Mar-a-Lago Club', type: 'Private Club/Resort', country: 'USA'},
        {id: 'manhattan_jail', name: 'Metropolitan Correctional Center', type: 'Federal Prison', country: 'USA'}
    ];
    renderLocations(locations);
    setupLocationSearch(locations);
}

function renderLocations(locations) {
    const container = document.querySelector('.locations-list');
    if (!container) return;
    
    container.innerHTML = '<h2>Key Locations</h2>';
    
    const grid = document.createElement('div');
    grid.className = 'locations-grid';
    
    locations.forEach(location => {
        const card = createLocationCard(location);
        grid.appendChild(card);
    });
    
    container.appendChild(grid);
}

function createLocationCard(location) {
    const article = document.createElement('article');
    article.className = 'location-card';
    article.setAttribute('data-type', location.type.toLowerCase().replace(/\s+/g, '-'));
    article.setAttribute('data-name', location.name.toLowerCase());
    
    const typeClass = location.type.toLowerCase().replace(/[\/\s]+/g, '-');
    
    article.innerHTML = `
        <div class="location-header">
            <h3><a href="locations/${location.id}.html">${location.name}</a></h3>
            <span class="location-tag tag-${typeClass}">${location.type}</span>
        </div>
        <div class="location-body">
            <p class="location-country">📍 ${location.country || 'Unknown'}</p>
            <a href="locations/${location.id}.html" class="view-location-btn">View Details →</a>
        </div>
    `;
    
    return article;
}

function setupLocationSearch(locations) {
    const searchInput = document.getElementById('location-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        filterLocations(query);
    });
}

function filterLocations(query) {
    const cards = document.querySelectorAll('.location-card');
    
    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const text = card.textContent.toLowerCase();
        
        if (name.includes(query) || text.includes(query)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// Add CSS for locations grid
const style = document.createElement('style');
style.textContent = `
    .locations-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .location-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .location-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .location-header {
        margin-bottom: 15px;
    }
    
    .location-header h3 {
        margin: 0 0 10px 0;
        font-size: 1.3em;
    }
    
    .location-header h3 a {
        color: #333;
        text-decoration: none;
    }
    
    .location-header h3 a:hover {
        color: #f5576c;
    }
    
    .location-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 500;
        background: #f5576c;
        color: white;
    }
    
    .location-country {
        color: #666;
        margin: 10px 0;
        font-size: 0.95em;
    }
    
    .view-location-btn {
        display: inline-block;
        padding: 8px 16px;
        background: #f5576c;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-size: 0.9em;
        transition: background 0.2s;
        margin-top: 10px;
    }
    
    .view-location-btn:hover {
        background: #e54858;
    }
`;
document.head.appendChild(style);
