/* eslint-env browser */
/* global window, document, fetch, localStorage, alert */
// Search functionality for Epstein Files Codex

const SEARCH_API_BASE_URL = window.EPSTEIN_API_BASE_URL || "";
let currentResults = [];

function getSearchEndpoint(path) {
    return `${SEARCH_API_BASE_URL}${path}`;
}

// Toggle advanced filters
function toggleAdvanced() {
    const advancedFilters = document.getElementById("advancedFilters");
    const toggleText = document.getElementById("toggleText");
    const toggleIcon = document.getElementById("toggleIcon");

    if (advancedFilters.style.display === "none" || !advancedFilters.style.display) {
        advancedFilters.style.display = "block";
        toggleText.textContent = "Hide Advanced Filters";
        toggleIcon.textContent = "▲";
    } else {
        advancedFilters.style.display = "none";
        toggleText.textContent = "Show Advanced Filters";
        toggleIcon.textContent = "▼";
    }
}

// Reset search form
function resetSearch() {
    const form = document.getElementById("searchForm");
    const container = document.getElementById("resultsContainer");
    const list = document.getElementById("resultsList");
    const count = document.getElementById("resultsCount");

    if (form) {
        form.reset();
    }
    if (container) {
        container.style.display = "none";
    }
    if (list) {
        list.innerHTML = "";
    }
    if (count) {
        count.textContent = "0 Results Found";
    }
    currentResults = [];
}

// Handle form submission
const searchForm = document.getElementById("searchForm");
if (searchForm) {
    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        performSearch();
    });
}

// Perform search (calls backend API)
async function performSearch() {
    const resultsContainer = document.getElementById("resultsContainer");
    const resultsList = document.getElementById("resultsList");
    const resultsCount = document.getElementById("resultsCount");

    resultsContainer.style.display = "block";
    resultsList.innerHTML = '<div class="loading-state">Searching files...</div>';

    const payload = collectFormData();
    try {
        const response = await fetch(getSearchEndpoint("/api/v1/search"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorBody = await response
                .json()
                .catch(() => ({ detail: "Search service unavailable" }));
            throw new Error(errorBody.detail || "Search request failed");
        }

        const responseBody = await response.json();
        currentResults = Array.isArray(responseBody.results)
            ? responseBody.results
            : [];

        displayResults(currentResults);
        resultsCount.textContent =
            `${responseBody.total} Result${responseBody.total !== 1 ? "s" : ""} Found`;
    } catch (error) {
        currentResults = [];
        resultsCount.textContent = "0 Results Found";
        resultsList.innerHTML = `
            <div class="no-results">
                <h3>Search temporarily unavailable</h3>
                <p>${escapeHtml(error.message)}</p>
                <button class="btn btn-primary" onclick="performSearch()">Retry</button>
            </div>
        `;
    }
}

function collectFormData() {
    const relevanceValue = document.getElementById("relevanceScore").value || "0";
    const sortBy = document.getElementById("sortBy")?.value || "relevance";

    return {
        keyword: document.getElementById("keyword").value,
        documentType: document.getElementById("documentType").value,
        dateFrom: document.getElementById("dateFrom").value,
        dateTo: document.getElementById("dateTo").value,
        location: document.getElementById("location").value,
        locationKeyword: document.getElementById("locationKeyword").value,
        redactionStatus: getSelectedCheckboxes("redaction"),
        person: document.getElementById("person")?.value || "",
        caseNumber: document.getElementById("caseNumber")?.value || "",
        fileSource: document.getElementById("fileSource")?.value || "",
        relevanceScore: parseInt(relevanceValue, 10),
        contentFlags: getSelectedCheckboxes("contentFlags"),
        sortBy,
        limit: 250,
        offset: 0,
    };
}

// Get selected checkbox values
function getSelectedCheckboxes(name) {
    const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    return Array.from(checkboxes).map((checkbox) => checkbox.value);
}

// Display search results
function displayResults(results) {
    const resultsList = document.getElementById("resultsList");

    if (results.length === 0) {
        resultsList.innerHTML = `
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try adjusting your search filters or using different keywords.</p>
            </div>
        `;
        return;
    }

    const resultsHtml = results
        .map((result) => {
            const title = escapeHtml(result.title || "Untitled");
            const type = escapeHtml(result.type || "Document");
            const location = escapeHtml(result.location || "Unknown");
            const redaction = escapeHtml(result.redaction || "Unknown");
            const caseNumber = result.caseNumber
                ? `<div class="result-case"><strong>Case Number:</strong> ${escapeHtml(result.caseNumber)}</div>`
                : "";
            const snippet = highlightKeywords(result.snippet || "");
            const tags = (result.tags || [])
                .map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`)
                .join("");

            return `
                <article class="result-card">
                    <div class="result-header">
                        <h3 class="result-title">${title}</h3>
                        <span class="result-type-badge">${type}</span>
                    </div>
                    <div class="result-meta">
                        <span class="meta-item"><strong>📅 Date:</strong> ${formatDate(result.date)}</span>
                        <span class="meta-item"><strong>📍 Location:</strong> ${location}</span>
                        <span class="meta-item"><strong>🔒 Status:</strong> ${redaction}</span>
                        <span class="meta-item"><strong>⭐ Relevance:</strong> ${result.relevance || 0}%</span>
                    </div>
                    ${caseNumber}
                    <p class="result-snippet">${snippet}</p>
                    <div class="result-tags">${tags}</div>
                    <div class="result-actions">
                        <button class="btn btn-sm btn-primary" onclick="viewDocument('${escapeHtml(result.id || "")}')">View Document</button>
                        <button class="btn btn-sm btn-secondary" onclick="addToCollection('${escapeHtml(result.id || "")}')">Add to Collection</button>
                    </div>
                </article>
            `;
        })
        .join("");

    resultsList.innerHTML = resultsHtml;
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) {
        return "Unknown";
    }

    const date = new Date(dateString);
    if (Number.isNaN(date.getTime())) {
        return escapeHtml(dateString);
    }

    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
}

// Highlight search keywords in results
function highlightKeywords(text) {
    const keyword = document.getElementById("keyword").value;
    const escapedText = escapeHtml(text);
    if (!keyword) {
        return escapedText;
    }

    const safeKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`(${safeKeyword})`, "gi");
    return escapedText.replace(regex, "<mark>$1</mark>");
}

// Sort results
function sortResults() {
    const sortBy = document.getElementById("sortBy").value;
    if (!currentResults.length) {
        return;
    }

    const sorted = [...currentResults];
    if (sortBy === "date-desc") {
        sorted.sort((a, b) => new Date(b.date) - new Date(a.date));
    } else if (sortBy === "date-asc") {
        sorted.sort((a, b) => new Date(a.date) - new Date(b.date));
    } else if (sortBy === "type") {
        sorted.sort((a, b) => (a.type || "").localeCompare(b.type || ""));
    } else if (sortBy === "location") {
        sorted.sort((a, b) => (a.location || "").localeCompare(b.location || ""));
    } else {
        sorted.sort((a, b) => (b.relevance || 0) - (a.relevance || 0));
    }

    displayResults(sorted);
}

// View document placeholder
function viewDocument(id) {
    window.location.href = `codex.html#${encodeURIComponent(id)}`;
}

// Add to collection placeholder
function addToCollection(id) {
    const key = "epstein_saved_documents";
    const existing = JSON.parse(localStorage.getItem(key) || "[]");
    if (!existing.includes(id)) {
        existing.push(id);
        localStorage.setItem(key, JSON.stringify(existing));
    }
    alert(`Saved ${id} to your local collection.`);
}

// Set search from example
function setSearch(query) {
    document.getElementById("keyword").value = query;
    performSearch();
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

// Update last updated timestamp
document.addEventListener("DOMContentLoaded", () => {
    const lastUpdatedElement = document.getElementById("lastUpdated");
    if (lastUpdatedElement) {
        lastUpdatedElement.textContent = new Date().toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }
});

// Expose handlers for inline HTML bindings
window.toggleAdvanced = toggleAdvanced;
window.resetSearch = resetSearch;
window.performSearch = performSearch;
window.sortResults = sortResults;
window.viewDocument = viewDocument;
window.addToCollection = addToCollection;
window.setSearch = setSearch;
