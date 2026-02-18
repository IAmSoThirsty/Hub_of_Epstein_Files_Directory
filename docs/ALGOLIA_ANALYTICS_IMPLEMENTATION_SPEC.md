"""
COMPREHENSIVE SYSTEM ARCHITECTURE AND IMPLEMENTATION SPECIFICATION
Epstein Files Hub: Algolia Integration and Advanced Analytics

This document provides maximum-detail, production-grade specifications for the
complete Algolia search integration and advanced analytics system, following
the strict mandate for concrete, real-world, technically correct implementation
over abstract description.

================================================================================
TABLE OF CONTENTS
================================================================================

1. EXECUTIVE SUMMARY AND SYSTEM OVERVIEW
2. COMPLETE TECHNOLOGY STACK SPECIFICATION
3. ARCHITECTURAL LAYERS AND COMPONENTS
4. DATA MODELS, SCHEMAS, AND PROTOCOLS
5. SECURITY ARCHITECTURE AND IMPLEMENTATION
6. CROSS-CUTTING CONCERNS
7. INFRASTRUCTURE AND DEPLOYMENT
8. OPERATIONAL PROCEDURES AND RUN

BOOKS
9. FAILURE MODES AND RECOVERY PATHS
10. GOVERNANCE, IDENTITY, AND DATA LIFECYCLE
11. PERFORMANCE AND SCALABILITY SPECIFICATIONS
12. MONITORING, OBSERVABILITY, AND ALERTING
13. TESTING AND QUALITY ASSURANCE
14. MIGRATION AND ROLLOUT STRATEGY
15. COST ANALYSIS AND RESOURCE PLANNING

================================================================================
1. EXECUTIVE SUMMARY AND SYSTEM OVERVIEW
================================================================================

1.1 SYSTEM PURPOSE
------------------
Production-grade search and analytics platform for the Epstein Files Hub,
enabling:
- Advanced full-text search across 30,000+ documents
- Real-time analytics on user behavior and content interaction
- Scalable infrastructure supporting 100K+ monthly active users
- Enterprise-grade security, compliance, and audit capabilities

1.2 KEY CAPABILITIES
--------------------
Search:
- Sub-100ms query response time at p99
- Typo-tolerant search with ML-powered relevance ranking
- Faceted filtering across 15+ dimensions
- Geolocation-based search for location entities
- Autocomplete and query suggestions
- Synonym management and semantic search

Analytics:
- Real-time event collection (10,000+ events/second capacity)
- User journey tracking and funnel analysis
- Content performance metrics and trending analysis
- Search analytics (queries, clicks, conversions)
- Custom dashboard and reporting
- Data export in CSV, JSON, Parquet formats

1.3 SYSTEM BOUNDARIES
---------------------
Trust Boundaries:
- User → Web Frontend (HTTPS/TLS 1.3)
- Web Frontend → Backend API (HTTPS/TLS 1.3 + API Key)
- Backend API → Algolia (HTTPS/TLS 1.3 + App-specific API Key)
- Backend API → Analytics Store (mTLS + KMS-encrypted connection)
- Admin → Admin Interface (HTTPS/TLS 1.3 + OAuth2 + RBAC)

Network Boundaries:
- Public Internet → Cloudflare CDN (DDoS protection, WAF)
- Cloudflare → GitHub Pages (Static assets)
- Backend Services → VPC (AWS/Azure) with security groups
- VPC → External Services (Algolia, Analytics) via NAT Gateway

Data Classification Boundaries:
- PUBLIC: Court documents, public figures information
- INTERNAL: Search analytics, aggregated user behavior
- CONFIDENTIAL: User PII, API keys, encryption keys
- RESTRICTED: Audit logs, security events

1.4 CORE ASSUMPTIONS
--------------------
Explicit Assumptions:
A1: Clock synchronization via NTP with <1s drift tolerance
A2: Network latency to Algolia <50ms at p95 (US East region)
A3: GitHub Pages uptime ≥99.9% per SLA
A4: Users have modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
A5: Peak traffic: 1,000 concurrent users, 10,000 searches/hour
A6: Data ingestion: 1,000 new documents/day average, 10,000/day peak
A7: Regulatory environment: US jurisdiction, GDPR awareness
A8: Budget constraint: $200-500/month operational costs

Impact of Assumption Violations:
- A1 violated → Analytics timestamps may be inconsistent, retry logic affected
- A2 violated → Search response times exceed SLA, circuit breaker may activate
- A3 violated → Static site unavailable, fallback to maintenance page
- A4 violated → Degraded UI experience, some features unavailable
- A5 violated → Rate limiting engaged, queue backlog increases
- A6 violated → Indexing jobs delayed, reindex operations needed
- A7 violated → Legal compliance requirements change, data retention affected
- A8 violated → Feature scaling limited, caching/storage optimization needed

================================================================================
2. COMPLETE TECHNOLOGY STACK SPECIFICATION
================================================================================

2.1 PROGRAMMING LANGUAGES AND RUNTIMES
---------------------------------------
Python Backend:
- Version: Python 3.11.8 (CPython)
- Rationale: Type hints, async/await, performance improvements
- Virtual Environment: venv with pip 24.0
- Package Manager: pip with pip-tools for dependency locking
- Minimum Version: Python 3.8+ (for compatibility)

JavaScript Frontend:
- Version: ES2022 (ECMAScript 13)
- Runtime: Browser-native (no Node.js required for production)
- Transpilation: Babel 7.24 for legacy browser support
- Module System: ES6 modules with dynamic imports
- Polyfills: core-js 3.36 for older browsers

TypeScript (Optional Enhancement):
- Version: TypeScript 5.3.3
- Configuration: strict mode, noImplicitAny
- Target: ES2020
- Use Case: Type-safe API client, complex UI components

2.2 FRAMEWORKS AND LIBRARIES
-----------------------------
Backend Python Frameworks:
- algoliasearch==3.0.0: Official Algolia Python client
  * Thread-safe client with connection pooling
  * Automatic retry with exponential backoff
  * Batch operations support

- pydantic==2.6.1: Data validation and settings management
  * Runtime type checking
  * JSON schema generation
  * Environment variable parsing

- FastAPI==0.109.2: Modern async API framework (if REST API needed)
  * OpenAPI/Swagger automatic documentation
  * Dependency injection
  * WebSocket support for real-time features

- tenacity==8.2.3: Retry logic with backoff strategies
  * Exponential backoff with jitter
  * Conditional retry policies
  * Async support

- circuitbreaker==1.4.0: Circuit breaker pattern implementation
  * State machine: CLOSED, OPEN, HALF_OPEN
  * Configurable failure thresholds
  * Recovery timeout management

- prometheus-client==0.19.0: Metrics collection and exposition
  * Counter, Gauge, Histogram, Summary metrics
  * Multi-process support
  * Push gateway integration

- redis==5.0.1: Redis client for caching and distributed locking
  * Connection pooling
  * Cluster support
  * Pub/sub for real-time events

- cryptography==42.0.2: Encryption and key management
  * Fernet symmetric encryption
  * PBKDF2 key derivation
  * X.509 certificate handling

- python-dotenv==1.0.1: Environment variable management
  * .env file loading
  * Variable interpolation
  * Multi-environment support

Frontend JavaScript Libraries:
- Algolia InstantSearch.js==4.61.0: Pre-built search UI components
  * Widgets: SearchBox, Hits, Pagination, RefinementList
  * Custom connector API
  * Server-side rendering support

- algoliasearch==4.22.1: JavaScript Algolia client
  * Lightweight (8KB gzipped)
  * Browser and Node.js compatible
  * Request caching

- Chart.js==4.4.1: Analytics visualization
  * Responsive charts
  * 8 chart types (line, bar, pie, etc.)
  * Canvas-based rendering

- D3.js==7.8.5: Advanced data visualization
  * Custom visualizations
  * SVG-based rendering
  * Data manipulation utilities

- Axios==1.6.7: HTTP client
  * Request/response interceptors
  * Automatic JSON transformation
  * CSRF token support

- Lodash==4.17.21: Utility functions
  * Debounce/throttle for search
  * Deep object manipulation
  * Array/collection operations

Monitoring and Observability:
- OpenTelemetry Python SDK==1.22.0: Distributed tracing
  * Trace context propagation
  * Span creation and attributes
  * Multiple exporter support

- structlog==24.1.0: Structured logging
  * JSON log formatting
  * Context binding
  * Performance optimized

- Sentry Python SDK==1.40.3: Error tracking and monitoring
  * Exception capture
  * Breadcrumbs
  * Performance monitoring

2.3 DATA STORAGE AND CACHING
-----------------------------
Primary Data Stores:
1. Algolia Indices (SaaS):
   - Provider: Algolia
   - Region: US-East-1 (primary), US-West-2 (replica)
   - Storage: Managed, distributed
   - Backup: Automatic snapshots, 30-day retention
   - Consistency: Eventually consistent (typically <1s)

2. PostgreSQL 16.2 (Analytics):
   - Provider: AWS RDS or Azure Database for PostgreSQL
   - Instance: db.t3.medium (2 vCPU, 4GB RAM) for budget tier
   - Storage: 100GB SSD (gp3) with auto-scaling to 500GB
   - Backup: Automated daily snapshots, 7-day retention, point-in-time recovery
   - Replication: Read replica in separate AZ for failover
   - Connection Pooling: PgBouncer with 100 max connections

3. Redis 7.2 (Cache and Session Store):
   - Provider: AWS ElastiCache or Azure Cache for Redis
   - Instance: cache.t3.micro (1 vCPU, 0.5GB RAM) for budget tier
   - Persistence: RDB snapshots every 5 minutes + AOF (appendonly)
   - Replication: Multi-AZ with automatic failover
   - Eviction Policy: allkeys-lru (least recently used)
   - Max Memory: 512MB with eviction at 90% threshold

Caching Strategy:
- L1 Cache (Memory): TTLCache with 1000 max entries, 1-hour TTL
  * Usage: Hot search queries
  * Invalidation: Time-based expiry
  * Memory Limit: 100MB

- L2 Cache (Redis): Distributed cache with 1-24 hour TTL
  * Usage: Search results, API responses, session data
  * Invalidation: Time-based + manual purge on data updates
  * Memory Limit: 512MB (expandable)

- L3 Cache (CDN): Cloudflare edge caching
  * Usage: Static assets, API responses with cache headers
  * TTL: 1 hour for API, 1 day for assets
  * Purge: API trigger on content updates

2.4 MESSAGE QUEUES AND STREAMING
---------------------------------
Message Queue:
- Technology: AWS SQS or Azure Queue Storage (budget tier)
  * Standard queues for async processing
  * Dead letter queues for failed messages
  * Message retention: 14 days
  * Max message size: 256KB
  * Visibility timeout: 30 seconds

- Alternative (Self-hosted): RabbitMQ 3.12
  * AMQP 0-9-1 protocol
  * Durable queues with persistence
  * Cluster deployment for HA
  * Management UI

Event Streaming (Future Enhancement):
- Technology: Apache Kafka 3.6 or AWS Kinesis
  * Topics: search_events, analytics_events, audit_logs
  * Partitions: 10 per topic for parallelism
  * Retention: 7 days
  * Compression: LZ4 or Snappy

2.5 INFRASTRUCTURE COMPONENTS
------------------------------
Web Hosting:
- Primary: GitHub Pages
  * Static site hosting
  * Custom domain support with HTTPS
  * 99.9% uptime SLA
  * 1GB soft limit per site

- CDN: Cloudflare Free/Pro Tier
  * Global edge network (275+ locations)
  * DDoS protection (Layer 3/4/7)
  * Web Application Firewall (WAF)
  * SSL/TLS termination (TLS 1.3)
  * Cache purge API
  * Rate limiting: 10,000 requests/minute (free tier)

Backend Hosting (Budget Tier):
- Option A: AWS EC2 t3.small
  * 2 vCPU, 2GB RAM
  * 30GB SSD root volume
  * Elastic IP
  * Auto Scaling Group: min=1, max=3, desired=1
  * Load Balancer: Application Load Balancer (ALB)

- Option B: Azure App Service B1
  * 1 core, 1.75GB RAM
  * 10GB storage
  * Built-in load balancing
  * Auto-scale based on CPU

- Option C: Docker containers on low-cost VPS
  * DigitalOcean Droplet: $12/month (2GB RAM, 1 vCPU)
  * Docker Compose orchestration
  * Nginx reverse proxy
  * Manual scaling

CI/CD:
- Platform: GitHub Actions
  * 2,000 minutes/month free
  * Linux, Windows, macOS runners
  * Self-hosted runners for cost optimization

- Workflows:
  1. Build & Test: On every push/PR
  2. Deploy to Staging: On merge to develop branch
  3. Deploy to Production: On merge to main branch
  4. Scheduled Jobs: Data indexing, analytics aggregation

Secret Management:
- Development: .env files (git-ignored)
- Staging/Production: GitHub Secrets + AWS Secrets Manager
  * KMS encryption
  * Automatic rotation for database credentials
  * IAM-based access control

2.6 MONITORING AND OBSERVABILITY STACK
---------------------------------------
Metrics:
- Collection: Prometheus 2.49
  * Scrape interval: 15 seconds
  * Retention: 15 days local, 1 year in remote storage
  * PromQL for queries

- Storage: AWS Managed Prometheus or Thanos
  * Long-term storage
  * Global query view
  * Downsampling

- Visualization: Grafana 10.3
  * Pre-built dashboards
  * Alerting rules
  * Organization-based multi-tenancy

Logs:
- Collection: Fluentd or Vector
  * Log parsing and enrichment
  * Multi-destination routing
  * Buffer management

- Storage: AWS CloudWatch Logs or ELK Stack
  * CloudWatch: $0.50/GB ingested, $0.03/GB stored
  * ELK: Elasticsearch 8.x + Kibana + Logstash
    - 3-node cluster for HA
    - Index lifecycle management
    - 30-day retention, then archive to S3

- Aggregation: structlog for structured JSON logs
  * Timestamp, level, logger, message, context
  * Request ID propagation

Tracing:
- Technology: OpenTelemetry + Jaeger
  * Distributed tracing across services
  * Trace sampling: 1% of requests (configurable)
  * Span attributes: user_id, request_id, operation
  * Context propagation via W3C Trace Context

Error Tracking:
- Technology: Sentry
  * Plan: Developer tier ($26/month) or self-hosted
  * Event volume: 50,000 errors/month
  * 90-day retention
  * Source map support for minified JS
  * Release tracking
  * Performance monitoring

Real User Monitoring (RUM):
- Technology: Browser-native Performance API + Custom beacon
  * Metrics: TTFB, FCP, LCP, FID, CLS
  * Collection endpoint: /api/rum
  * Sampling: 10% of sessions
  * Storage: Analytics database

Synthetic Monitoring:
- Technology: Uptime Robot (free tier) or Pingdom
  * HTTP checks every 5 minutes
  * 50 monitors on free tier
  * Email/SMS/Webhook alerts
  * Status page integration

Alerting:
- Technology: Grafana Alerting + PagerDuty
  * Alert rules in Prometheus/Grafana
  * Notification channels: Email, Slack, PagerDuty
  * Severity levels: P0 (critical), P1 (high), P2 (medium), P3 (low)
  * Escalation policies
  * On-call rotation

2.7 SECURITY INFRASTRUCTURE
----------------------------
Identity and Access Management:
- Authentication: OAuth 2.0 + OpenID Connect
  * Provider: Auth0 (free tier: 7,000 users) or self-hosted Keycloak
  * Protocols: Authorization Code Flow with PKCE
  * Session management: JWT with refresh tokens
  * Token expiry: Access token 1 hour, refresh token 30 days
  * MFA: TOTP (Google Authenticator, Authy)

- Authorization: RBAC (Role-Based Access Control)
  * Roles: anonymous, authenticated_user, contributor, moderator, admin
  * Permissions: read, write, delete, admin
  * Policy enforcement: Backend middleware + frontend guards

API Security:
- API Keys: SHA-256 hashed, stored in Secrets Manager
  * Format: prefix_32_char_random (e.g., sk_live_abc123...)
  * Rotation: Every 90 days (automated)
  * Rate limiting: per-key quotas

- mTLS (Mutual TLS):
  * Client certificates for service-to-service
  * Certificate authority: Internal PKI or Let's Encrypt
  * Certificate rotation: 90 days

Encryption:
- In Transit:
  * TLS 1.3 (minimum TLS 1.2)
  * Cipher suites: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256
  * HSTS: max-age=31536000; includeSubDomains; preload
  * Certificate pinning for mobile apps

- At Rest:
  * Database: AES-256-GCM (RDS encryption, Transparent Data Encryption)
  * File storage: S3 with SSE-KMS (AWS) or Azure Storage Service Encryption
  * Backups: Encrypted before upload
  * Secrets: AWS Secrets Manager with KMS, envelope encryption

Key Management:
- KMS: AWS KMS or Azure Key Vault
  * Customer managed keys (CMK)
  * Automatic key rotation: yearly
  * Key usage audit logging
  * Multi-region key replication

- HSM: AWS CloudHSM (for enhanced security, optional)
  * FIPS 140-2 Level 3 certified
  * Dedicated hardware
  * Cost: $1.60/hour + $0.14/hour per HSM user

Secrets Management:
- Tool: AWS Secrets Manager or HashiCorp Vault
  * Automatic rotation
  * Fine-grained access control
  * Audit logging
  * Versioning

Web Application Firewall (WAF):
- Provider: Cloudflare WAF or AWS WAF
  * OWASP Top 10 protection
  * Rate limiting: 100 requests/minute per IP
  * Geoblocking: Block specific countries if needed
  * Custom rules: SQL injection, XSS, CSRF
  * Bot management: Challenge-based verification

DDoS Protection:
- Layer 3/4: Cloudflare Magic Transit or AWS Shield Standard
  * Volumetric attack mitigation
  * SYN flood, UDP flood protection

- Layer 7: Cloudflare DDoS or AWS Shield Advanced
  * Application-layer attack mitigation
  * Cost-based protection ($3,000/month for Shield Advanced)

Security Scanning:
- SAST (Static Analysis): Bandit, Semgrep
  * Integrated in CI/CD pipeline
  * Scan on every commit
  * Block on critical vulnerabilities

- DAST (Dynamic Analysis): OWASP ZAP
  * Weekly scheduled scans
  * Authenticated scanning
  * API security testing

- Dependency Scanning: Dependabot, Snyk
  * Daily checks for vulnerable dependencies
  * Automated PR for updates
  * License compliance checking

- Container Scanning: Trivy, Clair
  * Scan Docker images before deployment
  * CVE database updates

Audit Logging:
- Events: Authentication, authorization, data access, configuration changes
- Format: JSON with timestamp, user, action, resource, IP, user-agent
- Storage: Immutable S3 bucket or Elasticsearch
- Retention: 1 year (compliance requirement)
- SIEM Integration: Splunk, Sumo Logic, or AWS Security Hub

================================================================================
3. ARCHITECTURAL LAYERS AND COMPONENTS
================================================================================

3.1 PRESENTATION LAYER
----------------------

3.1.1 Web Frontend Architecture
Deployment:
- Static files hosted on GitHub Pages
- Assets served via Cloudflare CDN
- URL: https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/

Directory Structure:
```
web/
├── index.html                 # Home page
├── search.html                # Search interface with Algolia
├── analytics-dashboard.html   # Analytics dashboard (admin)
├── characters.html            # Character directory
├── locations.html             # Locations directory
├── infographics.html          # Visual content
├── css/
│   ├── styles.css            # Main stylesheet
│   ├── search.css            # Search-specific styles
│   ├── analytics.css         # Analytics dashboard styles
│   └── components/           # Component-specific styles
├── js/
│   ├── main.js               # Core application logic
│   ├── algolia-search.js     # Algolia search integration
│   ├── algolia-analytics.js  # Analytics collection
│   ├── search-ui.js          # Search UI components
│   ├── analytics-dashboard.js # Dashboard logic
│   ├── chart-config.js       # Chart.js configurations
│   └── api-client.js         # Backend API client
├── assets/
│   ├── images/               # Static images
│   ├── icons/                # SVG icons
│   └── fonts/                # Custom fonts
└── sw.js                      # Service worker for PWA
```

HTML Structure (search.html example):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Search 30,000+ Epstein Files">

    <!-- Security Headers -->
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self';
                   script-src 'self' https://cdn.jsdelivr.net https://*.algolia.net 'unsafe-inline';
                   style-src 'self' 'unsafe-inline';
                   connect-src 'self' https://*.algolia.net https://*.algolianet.com;
                   img-src 'self' data: https:;">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="X-XSS-Protection" content="1; mode=block">
    <meta name="referrer" content="strict-origin-when-cross-origin">

    <title>Search - Epstein Files Codex</title>

    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://cdn.jsdelivr.net">
    <link rel="preconnect" href="https://APPID-dsn.algolia.net">

    <!-- Stylesheets -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/search.css">

    <!-- Algolia InstantSearch CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/instantsearch.css@8/themes/algolia-min.css">
</head>
<body>
    <nav><!-- Navigation --></nav>

    <main id="search-container">
        <!-- Algolia InstantSearch widgets will be mounted here -->
        <div id="searchbox"></div>
        <div id="stats"></div>
        <div id="hits"></div>
        <div id="pagination"></div>
        <div id="refinement-list"></div>
    </main>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/algoliasearch@4/dist/algoliasearch-lite.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/instantsearch.js@4"></script>
    <script src="js/algolia-search.js" type="module"></script>
    <script src="js/algolia-analytics.js" type="module"></script>
</body>
</html>
```

JavaScript Module Structure (algolia-search.js):
```javascript
// Configuration
const ALGOLIA_CONFIG = {
    appId: 'YOUR_APP_ID',  // Loaded from meta tag or env
    apiKey: 'SEARCH_ONLY_API_KEY',  // Search-only key (safe for frontend)
    indexName: 'prod_documents'
};

// Initialize Algolia client
const searchClient = algoliasearch(
    ALGOLIA_CONFIG.appId,
    ALGOLIA_CONFIG.apiKey
);

// Initialize InstantSearch
const search = instantsearch({
    indexName: ALGOLIA_CONFIG.indexName,
    searchClient,
    routing: true,  // URL routing for SEO
    insights: true,  // Enable analytics
});

// Add widgets
search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
        placeholder: 'Search documents...',
        showSubmit: false,
        showReset: true,
        autofocus: true,
    }),

    instantsearch.widgets.stats({
        container: '#stats',
        templates: {
            text: '{{nbHits}} results found in {{processingTimeMS}}ms',
        },
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `
                <article class="hit">
                    <h3>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</h3>
                    <p class="hit-date">{{date}}</p>
                    <p class="hit-snippet">{{#helpers.snippet}}{ "attribute": "content", "highlightedTagName": "mark" }{{/helpers.snippet}}</p>
                    <div class="hit-meta">
                        <span class="hit-type">{{type}}</span>
                        <span class="hit-location">{{location}}</span>
                    </div>
                </article>
            `,
        },
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list',
        attribute: 'type',
        limit: 10,
        showMore: true,
        searchable: true,
    }),

    instantsearch.widgets.pagination({
        container: '#pagination',
        padding: 2,
        showFirst: false,
        showLast: false,
    }),
]);

// Start search
search.start();

// Analytics tracking
search.on('render', () => {
    trackSearchRender(search.helper.state);
});

function trackSearchRender(state) {
    // Send analytics event to backend
    if (window.analyticsEnabled) {
        fetch('/api/analytics/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: state.query,
                filters: state.disjunctiveFacetsRefinements,
                timestamp: new Date().toISOString(),
                session_id: getSessionId(),
            }),
        }).catch(err => console.error('Analytics tracking failed:', err));
    }
}
```

3.1.2 Progressive Web App (PWA) Features
Service Worker (sw.js):
```javascript
const CACHE_VERSION = 'v1.0.0';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;
const SEARCH_CACHE = `search-${CACHE_VERSION}`;

// Assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/search.html',
    '/css/styles.css',
    '/js/main.js',
    '/js/algolia-search.js',
    '/assets/logo.svg',
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

// Activate event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter(key => key !== STATIC_CACHE && key !== DYNAMIC_CACHE && key !== SEARCH_CACHE)
                    .map(key => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event with network-first strategy for search, cache-first for static
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Algolia API requests - network-first with cache fallback
    if (url.hostname.includes('algolia.net') || url.hostname.includes('algolianet.com')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    const clonedResponse = response.clone();
                    caches.open(SEARCH_CACHE).then(cache => {
                        cache.put(request, clonedResponse);
                    });
                    return response;
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // Static assets - cache-first
    if (STATIC_ASSETS.includes(url.pathname)) {
        event.respondWith(
            caches.match(request)
                .then(response => response || fetch(request))
        );
        return;
    }

    // Other requests - network-first with dynamic cache
    event.respondWith(
        fetch(request)
            .then(response => {
                const clonedResponse = response.clone();
                caches.open(DYNAMIC_CACHE).then(cache => {
                    cache.put(request, clonedResponse);
                });
                return response;
            })
            .catch(() => caches.match(request))
    );
});
```

Web App Manifest (manifest.json):
```json
{
    "name": "Epstein Files Codex",
    "short_name": "EF Codex",
    "description": "Comprehensive directory of Epstein-related files",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#1a1a2e",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "/assets/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "/assets/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
}
```

3.2 APPLICATION LAYER
----------------------

3.2.1 Backend API Architecture (FastAPI)
File Structure:
```
api/
├── main.py                    # FastAPI application entry
├── config.py                  # Configuration management
├── dependencies.py            # Dependency injection
├── middleware/
│   ├── auth.py               # Authentication middleware
│   ├── rate_limit.py         # Rate limiting middleware
│   ├── cors.py               # CORS configuration
│   └── logging.py            # Request/response logging
├── routers/
│   ├── search.py             # Search endpoints
│   ├── analytics.py          # Analytics endpoints
│   ├── admin.py              # Admin endpoints
│   └── health.py             # Health check endpoints
├── models/
│   ├── search.py             # Search request/response models
│   ├── analytics.py          # Analytics event models
│   └── user.py               # User models
├── services/
│   ├── algolia_service.py    # Algolia integration service
│   ├── analytics_service.py  # Analytics processing service
│   └── auth_service.py       # Authentication service
├── utils/
│   ├── cache.py              # Caching utilities
│   ├── metrics.py            # Prometheus metrics
│   └── validators.py         # Input validation
└── tests/
    ├── test_search.py
    ├── test_analytics.py
    └── test_integration.py
```

Main Application (main.py):
```python
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

from api.routers import search, analytics, admin, health
from api.middleware.auth import AuthMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.logging import LoggingMiddleware
from api.config import settings
from api.dependencies import get_db, get_redis, get_algolia_client

# Initialize FastAPI app
app = FastAPI(
    title="Epstein Files Hub API",
    description="Production-grade search and analytics API",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # ["https://iamsothirsty.github.io"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware, redis_client=get_redis())
app.add_middleware(LoggingMiddleware)

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request.state.request_id,
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting API server (environment={settings.ENVIRONMENT})")
    # Initialize connections
    await get_db().connect()
    await get_redis().ping()
    # Validate Algolia connection
    algolia_client = get_algolia_client()
    algolia_client.list_indices()
    logger.info("API server started successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API server")
    await get_db().disconnect()
    await get_redis().close()
    logger.info("API server shut down complete")

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        workers=4 if settings.ENVIRONMENT == "production" else 1,
        log_config=settings.LOGGING_CONFIG,
        access_log=True,
    )
```

Search Router (routers/search.py):
```python
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field

from api.services.algolia_service import AlgoliaService
from api.dependencies import get_algolia_service, get_current_user
from api.models.search import SearchRequest, SearchResponse
from api.utils.cache import cache
from api.utils.metrics import search_request_counter, search_duration_histogram

router = APIRouter()

@router.post("/", response_model=SearchResponse)
@search_duration_histogram.time()
async def search_documents(
    request: SearchRequest,
    algolia_service: AlgoliaService = Depends(get_algolia_service),
    current_user: Optional[dict] = Depends(get_current_user),
):
    """
    Search documents with advanced filtering.

    **Request Body:**
    ```json
    {
        "query": "flight logs",
        "filters": {
            "date_from": "2000-01-01",
            "location": "Little St. James"
        },
        "page": 0,
        "hits_per_page": 20,
        "facets": ["type", "location", "date"]
    }
    ```

    **Response:**
    ```json
    {
        "hits": [...],
        "total_hits": 150,
        "page": 0,
        "total_pages": 8,
        "processing_time_ms": 12,
        "facets": {...}
    }
    ```

    **Rate Limit:** 100 requests/minute per API key
    **Cache TTL:** 1 hour
    """
    try:
        # Generate cache key
        cache_key = f"search:{request.get_cache_key()}"

        # Check cache
        cached_result = await cache.get(cache_key)
        if cached_result:
            search_request_counter.labels(status="cache_hit").inc()
            return SearchResponse.parse_raw(cached_result)

        # Execute search
        result = await algolia_service.search(
            index_type=request.index_type,
            query=request.query,
            filters=request.filters,
            page=request.page,
            hits_per_page=request.hits_per_page,
            facets=request.facets,
            user_token=current_user.get("id") if current_user else None,
        )

        # Cache result
        await cache.set(cache_key, result.json(), ttl=3600)

        search_request_counter.labels(status="success").inc()
        return result

    except Exception as e:
        search_request_counter.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete", response_model=List[str])
async def autocomplete(
    query: str = Query(..., min_length=2, max_length=100),
    limit: int = Query(10, ge=1, le=50),
    algolia_service: AlgoliaService = Depends(get_algolia_service),
):
    """
    Get autocomplete suggestions.

    **Query Parameters:**
    - query: Search prefix (min 2 characters)
    - limit: Max suggestions (default 10, max 50)

    **Response:**
    ```json
    ["flight logs", "flight manifest", "florida estate"]
    ```

    **Rate Limit:** 200 requests/minute per API key
    **Cache TTL:** 6 hours
    """
    try:
        suggestions = await algolia_service.get_autocomplete(query, limit)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/track-click")
async def track_click(
    query_id: str,
    object_id: str,
    position: int,
    algolia_service: AlgoliaService = Depends(get_algolia_service),
    current_user: Optional[dict] = Depends(get_current_user),
):
    """
    Track click event for search analytics.

    **Request Body:**
    ```json
    {
        "query_id": "abc123",
        "object_id": "doc_456",
        "position": 3
    }
    ```

    **Algolia Insights:** This data is sent to Algolia Insights API
    for search analytics and relevance optimization.
    """
    try:
        await algolia_service.track_click(
            query_id=query_id,
            object_id=object_id,
            position=position,
            user_token=current_user.get("id") if current_user else None,
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Analytics Router (routers/analytics.py):
```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime, timedelta

from api.services.analytics_service import AnalyticsService
from api.dependencies import get_analytics_service, require_admin
from api.models.analytics import (
    AnalyticsEvent,
    AnalyticsQuery,
    AnalyticsReport,
    EventType,
)

router = APIRouter()

@router.post("/events")
async def track_event(
    event: AnalyticsEvent,
    background_tasks: BackgroundTasks,
    analytics_service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Track analytics event.

    **Request Body:**
    ```json
    {
        "event_type": "page_view",
        "event_data": {
            "page": "/search",
            "referrer": "https://example.com"
        },
        "user_id": "user_123",
        "session_id": "session_456",
        "timestamp": "2026-02-18T12:00:00Z"
    }
    ```

    **Event Types:**
    - page_view
    - search
    - click
    - download
    - share
    - error

    **Processing:** Events are processed asynchronously in background.
    """
    # Validate event
    if not event.validate():
        raise HTTPException(status_code=400, detail="Invalid event data")

    # Queue event for processing
    background_tasks.add_task(
        analytics_service.process_event,
        event
    )

    return {"status": "accepted", "event_id": event.event_id}

@router.get("/report", response_model=AnalyticsReport)
async def get_analytics_report(
    start_date: datetime,
    end_date: datetime,
    metrics: List[str] = Query(["page_views", "searches", "unique_users"]),
    granularity: str = Query("day", regex="^(hour|day|week|month)$"),
    analytics_service: AnalyticsService = Depends(get_analytics_service),
    _admin: dict = Depends(require_admin),
):
    """
    Get analytics report (admin only).

    **Query Parameters:**
    - start_date: Report start date (ISO 8601)
    - end_date: Report end date (ISO 8601)
    - metrics: List of metrics to include
    - granularity: Aggregation granularity (hour, day, week, month)

    **Response:**
    ```json
    {
        "period": {
            "start": "2026-02-01T00:00:00Z",
            "end": "2026-02-18T23:59:59Z"
        },
        "metrics": {
            "page_views": 125000,
            "searches": 45000,
            "unique_users": 12500
        },
        "timeseries": [
            {
                "timestamp": "2026-02-01T00:00:00Z",
                "page_views": 5000,
                "searches": 1800,
                "unique_users": 500
            },
            ...
        ]
    }
    ```
    """
    try:
        report = await analytics_service.generate_report(
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            granularity=granularity,
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

(Continued in next section due to length...)

================================================================================
TO BE CONTINUED...

This document will continue with:
- Section 3.3: Data Layer implementation details
- Section 4: Complete data models and schemas
- Section 5: Security implementation details
- Sections 6-15: All remaining architectural components

Each section will provide the same level of maximum technical detail with
concrete implementation code, configurations, protocols, and operational
procedures.
================================================================================
"""
