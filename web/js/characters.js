/**
 * Dynamic Character Loader
 * Loads all character profiles from the generated database
 */

document.addEventListener('DOMContentLoaded', function() {
    // Load character data
    fetch('data/characters_index.json')
        .then(response => response.json())
        .then(characters => {
            renderCharacters(characters);
            setupSearch(characters);
            setupFilters(characters);
        })
        .catch(error => {
            console.error('Error loading characters:', error);
            showFallbackContent();
        });
});

function renderCharacters(characters) {
    const container = document.querySelector('.characters-list');
    if (!container) return;
    
    // Clear existing content except the header
    const existingHeader = container.querySelector('h2');
    container.innerHTML = '';
    if (existingHeader) {
        container.appendChild(existingHeader);
    }
    
    // Group characters by role
    const grouped = groupByRole(characters);
    
    // Render each group
    Object.keys(grouped).forEach(role => {
        const section = document.createElement('section');
        section.className = 'character-group';
        
        const header = document.createElement('h2');
        header.textContent = role;
        section.appendChild(header);
        
        const grid = document.createElement('div');
        grid.className = 'character-grid';
        
        grouped[role].forEach(character => {
            const card = createCharacterCard(character);
            grid.appendChild(card);
        });
        
        section.appendChild(grid);
        container.appendChild(section);
    });
}

function groupByRole(characters) {
    const groups = {};
    
    characters.forEach(char => {
        const role = char.role || 'Other';
        if (!groups[role]) {
            groups[role] = [];
        }
        groups[role].push(char);
    });
    
    // Sort groups by priority
    const priority = ['Primary Subject', 'Victim & Witness', 'Associate', 'Legal Counsel', 'Legal Personnel', 'Business Associate', 'Political Figure'];
    const sorted = {};
    
    priority.forEach(role => {
        if (groups[role]) {
            sorted[role] = groups[role];
        }
    });
    
    // Add remaining roles
    Object.keys(groups).forEach(role => {
        if (!sorted[role]) {
            sorted[role] = groups[role];
        }
    });
    
    return sorted;
}

function createCharacterCard(character) {
    const article = document.createElement('article');
    article.className = 'character-card';
    article.setAttribute('data-role', character.role.toLowerCase().replace(/\s+/g, '-'));
    article.setAttribute('data-name', character.name.toLowerCase());
    
    const roleClass = character.role.toLowerCase().replace(/\s+/g, '-');
    
    article.innerHTML = `
        <div class="character-header">
            <h3><a href="profiles/${character.id}.html">${character.name}</a></h3>
            <span class="character-tag tag-${roleClass}">${character.role}</span>
        </div>
        <div class="character-body">
            <p class="character-summary">${character.summary}</p>
            <a href="profiles/${character.id}.html" class="view-profile-btn">View Full Profile →</a>
        </div>
    `;
    
    return article;
}

function setupSearch(characters) {
    const searchInput = document.getElementById('character-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        filterCharacters(characters, query);
    });
}

function setupFilters(characters) {
    const roleFilter = document.getElementById('role-filter');
    const sortSelect = document.getElementById('sort-select');
    
    if (roleFilter) {
        roleFilter.addEventListener('change', function() {
            applyFilters(characters);
        });
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            applyFilters(characters);
        });
    }
}

function filterCharacters(characters, query) {
    const cards = document.querySelectorAll('.character-card');
    
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

function applyFilters(characters) {
    const roleFilter = document.getElementById('role-filter');
    const sortSelect = document.getElementById('sort-select');
    
    let filtered = [...characters];
    
    // Apply role filter
    if (roleFilter && roleFilter.value !== 'all') {
        const roleMap = {
            'subject': 'Primary Subject',
            'legal': 'Legal',
            'witness': 'Witness',
            'victim': 'Victim',
            'investigator': 'Investigator',
            'associate': 'Associate',
            'political': 'Political',
            'business': 'Business'
        };
        
        const selectedRole = roleMap[roleFilter.value];
        filtered = filtered.filter(char => char.role.includes(selectedRole));
    }
    
    // Apply sorting
    if (sortSelect) {
        switch(sortSelect.value) {
            case 'alpha':
                filtered.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'relevance':
                // Keep default order
                break;
            case 'category':
                filtered.sort((a, b) => a.role.localeCompare(b.role));
                break;
        }
    }
    
    renderCharacters(filtered);
}

function showFallbackContent() {
    const container = document.querySelector('.characters-list');
    if (!container) return;
    
    container.innerHTML = `
        <div class="error-message">
            <h3>⚠️ Unable to load character data</h3>
            <p>Please check your connection and refresh the page.</p>
        </div>
    `;
}

// Add CSS for character grid
const style = document.createElement('style');
style.textContent = `
    .character-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .character-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .character-header {
        margin-bottom: 15px;
    }
    
    .character-header h3 {
        margin: 0 0 10px 0;
        font-size: 1.3em;
    }
    
    .character-header h3 a {
        color: #333;
        text-decoration: none;
    }
    
    .character-header h3 a:hover {
        color: #667eea;
    }
    
    .character-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 500;
        margin-right: 5px;
    }
    
    .tag-primary-subject {
        background: #ff6b6b;
        color: white;
    }
    
    .tag-victim-&-witness {
        background: #4ecdc4;
        color: white;
    }
    
    .tag-associate {
        background: #feca57;
        color: #333;
    }
    
    .tag-legal-counsel,
    .tag-legal-personnel {
        background: #48dbfb;
        color: white;
    }
    
    .tag-business-associate {
        background: #ff9ff3;
        color: white;
    }
    
    .tag-political-figure {
        background: #54a0ff;
        color: white;
    }
    
    .character-summary {
        color: #666;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    
    .view-profile-btn {
        display: inline-block;
        padding: 8px 16px;
        background: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-size: 0.9em;
        transition: background 0.2s;
    }
    
    .view-profile-btn:hover {
        background: #5568d3;
    }
    
    .character-group {
        margin: 40px 0;
    }
    
    .character-group h2 {
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .error-message {
        text-align: center;
        padding: 40px;
        background: #fff3cd;
        border-radius: 8px;
        border: 2px solid #ffc107;
    }
`;
document.head.appendChild(style);
