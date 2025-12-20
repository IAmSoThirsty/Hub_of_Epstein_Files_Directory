# Epstein Files Hub - Quick Start Guide

## Product Description

**Epstein Files Hub** is a comprehensive, FREE ($0/month) document management and search platform for 30,000+ documents and 20,000+ images related to the Epstein case. Built with GitHub Pages, it features advanced search capabilities, automated data collection from official sources (FBI Vault, DOJ, Wikipedia), 26 AI agents for document processing, staff collaboration portal, and volunteer management system.

**Key Features:**
- ✅ Advanced search with 15+ filters (dates, locations, redaction status, persons, cases)
- ✅ Real-time AI agent monitoring and task assignment
- ✅ Staff portal with private chat, calendar, and bulletin board
- ✅ Automated FBI Vault (22 PDFs) and DOJ flight log integration
- ✅ Wikipedia data integration (15+ articles with dates, locations, characters)
- ✅ Owner-only access control with volunteer application system
- ✅ Completely FREE hosting with GitHub Pages

**Monthly Cost:** $0 (saves $15,720+/year vs. Azure)

---

## Deployment Instructions

### Prerequisites

```bash
# Required software
- Python 3.8+
- Git
- GitHub account with admin access to this repository
```

### Step 1: Deploy Site (5 minutes)

1. **Enable GitHub Pages:**
   - Go to repository **Settings** → **Pages**
   - Set **Source** to: Branch `copilot/create-self-organizing-workflow`, Folder `/web`
   - Click **Save**
   - Wait 2-3 minutes for deployment

2. **Your site is live at:**
   ```
   https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/
   ```

3. **Verify deployment:**
   - Visit the URL above
   - You should see the home page with navigation menu
   - Test the search page

### Step 2: Set Up Access Control (10 minutes)

1. **Enable Branch Protection:**
   - Go to **Settings** → **Branches**
   - Click **Add rule**
   - Branch name pattern: `main`
   - Check:
     - ✅ Require pull request reviews before merging
     - ✅ Require review from Code Owners
     - ✅ Dismiss stale pull request approvals
     - ✅ Include administrators
     - ✅ Restrict who can push (add yourself only)
   - Click **Create**

2. **Verify CODEOWNERS:**
   - File already created at `.github/CODEOWNERS`
   - All PRs will require your review

3. **Enable Volunteer Workflow (Optional):**
   - Go to **Actions** → **Volunteer Application Handler**
   - Click **Enable workflow**

### Step 3: Set Up Staff Portal (15 minutes)

1. **Install dependencies:**
   ```bash
   cd /path/to/repository
   pip install -r requirements.txt
   ```

2. **Run setup script:**
   ```bash
   python scripts/setup-staff-portal.py
   ```
   - Follow prompts to configure portal

3. **Create GitHub OAuth App:**
   - Visit: https://github.com/settings/developers
   - Click **New OAuth App**
   - Fill in:
     - **Application name:** Epstein Files Hub Staff Portal
     - **Homepage URL:** `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/`
     - **Authorization callback URL:** `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/staff/callback`
   - Click **Register application**
   - Copy **Client ID** and **Client Secret**

4. **Configure credentials:**
   - Create `.env` file in repository root:
   ```bash
   GITHUB_OAUTH_CLIENT_ID=your_client_id_here
   GITHUB_OAUTH_CLIENT_SECRET=your_client_secret_here
   GITHUB_OAUTH_CALLBACK_URL=https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/staff/callback
   ```
   - **IMPORTANT:** Never commit `.env` file (already in `.gitignore`)

5. **Access staff portal:**
   - Visit: `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/staff/login.html`
   - Click **Login with GitHub**
   - Grant permissions
   - You're now logged in as Admin

### Step 4: Integrate Public Data Sources (2 hours)

1. **Fetch FBI Vault documents (22 PDFs):**
   ```bash
   python scripts/fetch-public-files.py
   ```
   - Downloads all 22 FBI Vault PDFs (~300MB)
   - Extracts metadata (dates, locations, persons)
   - SHA-256 verification for integrity
   - Saves to `data/public_files/fbi_vault/`

2. **Fetch Wikipedia data (15+ articles):**
   ```bash
   python scripts/fetch-wikipedia-data.py
   ```
   - Fetches 15+ Wikipedia articles
   - Extracts dates, times, locations, characters
   - Generates profiles, timeline, location guide
   - Saves to `data/wikipedia/`

3. **Run safe source discovery (optional):**
   ```bash
   python scripts/safe-source-expander.py
   ```
   - Monitors 5 official sources (Archive.org, DocumentCloud, Wikimedia, DOJ RSS, FBI RSS)
   - Creates GitHub Issue with findings
   - You approve items by commenting on issue

4. **Process PDFs:**
   ```bash
   python scripts/process-pdfs.py
   ```
   - Extracts text from all PDFs
   - Runs OCR on scanned documents (requires Tesseract)
   - Extracts metadata (dates, case numbers, locations)
   - Saves to `data/processed/`

5. **Generate search index:**
   ```bash
   python scripts/generate-search-index.py
   ```
   - Creates searchable index for Lunr.js
   - Includes all documents and metadata
   - Saves to `web/js/search-index.js`

6. **Deploy updates:**
   ```bash
   git add data/ web/js/search-index.js
   git commit -m "Add public files and search index"
   git push
   ```
   - GitHub Pages will auto-deploy in 2-3 minutes

### Step 5: Enable Automated Workflows (5 minutes)

1. **Enable workflows:**
   - Go to **Actions** tab
   - Enable the following workflows:
     - ✅ **Fetch and Process Public Files** (Monthly: FBI/DOJ)
     - ✅ **Wikipedia Integration** (Weekly: Sundays 3 AM UTC)
     - ✅ **Source Discovery** (Daily: 2 AM UTC)
     - ✅ **Update Search Index** (Weekly: After data updates)

2. **Verify schedules:**
   - FBI/DOJ: 1st of each month at 2 AM UTC
   - Wikipedia: Every Sunday at 3 AM UTC
   - Source Discovery: Daily at 2 AM UTC with approval required

### Step 6: Add Staff Members (10 minutes)

1. **Login as Admin:**
   - Visit: `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/staff/login.html`

2. **Go to Admin Panel:**
   - Click **Admin** in staff portal navigation

3. **Add staff member:**
   - Click **Add Staff Member**
   - Enter GitHub username
   - Assign role: Staff, Editor, or Admin
   - Click **Save**
   - User will receive email invitation

4. **Role permissions:**
   - **Staff:** View agents, chat, calendar, assign tasks
   - **Editor:** Same as Staff + post to bulletin board + create calendar events
   - **Admin:** Full control including AI agent management (you only)

---

## Staff Portal Features

### Access Staff Portal
- **URL:** `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/staff/login.html`
- **Login:** Click "Login with GitHub"

### Available Features

1. **Dashboard** (`/staff/dashboard.html`)
   - Welcome panel with user info
   - Quick links to all features
   - Recent activity feed
   - Notifications panel

2. **Private Chat** (`/staff/chat.html`)
   - 4 rooms: General, Research, Technical, Support
   - Direct messages between staff
   - @mentions and notifications
   - File attachments support
   - Real-time updates (every 5 seconds)

3. **Team Calendar** (`/staff/calendar.html`)
   - **Set Availability:** Click any day to set status
     - Available (green), Partial (yellow), Busy (red), Off (gray)
   - Add time ranges and notes
   - Create events (Editor/Admin only)
   - View team availability at a glance

4. **Task Assignment** (`/staff/tasks.html`)
   - Select AI agent from 26 available
   - Set priority: High, Medium, Low
   - Tasks queue up and process by priority
   - Real-time queue display
   - GitHub Issue created for each task

5. **Bulletin Board** (`/staff/bulletin.html`)
   - View announcements (all staff)
   - Post updates (Editor/Admin only)
   - Pin important posts (Admin only)
   - Rich markdown formatting

6. **AI Agent Dashboard** (`/staff/agents.html`)
   - Real-time status of all 26 agents
   - Visual indicators (Active/Idle/Error)
   - Current tasks display
   - Performance metrics
   - Admin controls (Admin only)

7. **Staff Management** (`/staff/admin.html`) - Admin only
   - Add/remove staff members
   - Assign roles
   - View activity logs
   - Monitor access

---

## Public Interface Features

### Public Pages (No login required)

1. **Home** (`/index.html`)
   - Overview and feature cards
   - Quick navigation
   - Recent updates

2. **Search** (`/search.html`)
   - 15+ search filters
   - Date range filtering
   - Location filtering
   - Redaction status
   - Person mentions
   - Case numbers
   - Content flags
   - Real-time results

3. **Character Guide** (`/characters.html`)
   - 350+ individual profiles
   - Wikipedia-enhanced data
   - Relationships and connections
   - Timeline of involvement

4. **Locations** (`/locations.html`)
   - 50+ significant locations
   - Addresses and coordinates
   - Associated persons
   - Significance details

5. **Infographics** (`/infographics.html`)
   - Visual relationship mapping
   - Timeline graphics
   - Network diagrams

6. **Slideshows** (`/slideshow.html`)
   - Curated presentations
   - Key evidence displays

7. **Codex** (`/codex.html`)
   - AI-curated document browser
   - Organized by category

8. **Upload** (`/upload.html`)
   - PDF submission interface
   - Auto-analysis (70% relevance threshold)
   - Automatic routing

9. **Volunteer Application** (`/volunteer.html`)
   - Online application form
   - Role selection
   - Background check consent
   - Creates GitHub Issue for review

---

## Volunteer Management

### Accepting Volunteers

1. **Volunteer submits application:**
   - Via `/volunteer.html` form
   - GitHub Issue created automatically

2. **Review application:**
   - Go to **Issues** tab
   - Find issue titled "Volunteer Application: [Name]"
   - Review qualifications

3. **Approve or reject:**
   - Comment on issue:
     - `approve: level-2` (Viewer - read only)
     - `approve: level-3` (Contributor - submit PRs)
     - `approve: level-4` (Editor - broader PR permissions)
     - `reject: reason` (Deny application)

4. **Bot processes decision:**
   - Sends instructions to volunteer
   - Volunteer forks repository
   - Volunteer submits pull requests

5. **Review volunteer PRs:**
   - You receive notification
   - Review changes carefully
   - Approve and merge or request changes
   - Your approval required for every change

### Volunteer Permissions

- **Level 1 (Applicant):** No access until approved
- **Level 2 (Viewer):** Read-only access to public pages
- **Level 3 (Contributor):** Can submit pull requests
- **Level 4 (Editor):** Can edit multiple files via PR
- **Level 5 (Administrator):** Reserved for you only

---

## Automated Data Collection

### What's Automated (No action needed)

1. **FBI Vault (Monthly):**
   - 1st of each month at 2 AM UTC
   - Fetches all 22 PDFs
   - Processes with OCR
   - Updates search index

2. **Wikipedia (Weekly):**
   - Every Sunday at 3 AM UTC
   - Fetches 15+ articles
   - Extracts dates, locations, persons
   - Updates profiles and timeline

3. **Source Discovery (Daily):**
   - Every day at 2 AM UTC
   - Monitors 5 official sources
   - Creates GitHub Issue with findings
   - **Requires your approval** to download

### Approving Discovered Sources

1. **Check GitHub Issues daily:**
   - Look for "Source Discovery Report" issues

2. **Review findings:**
   - Each item includes:
     - Source name and URL
     - Description
     - Relevance score
     - File type and size

3. **Approve items:**
   - Comment: `approve: item-1,item-3,item-5`
   - Bot downloads approved items
   - Processes and indexes automatically

---

## Troubleshooting

### Site not deploying

1. Check GitHub Pages settings
2. Ensure branch is `copilot/create-self-organizing-workflow`
3. Ensure folder is `/web`
4. Check Actions tab for deployment errors

### Staff portal login not working

1. Verify OAuth app credentials in `.env`
2. Check callback URL matches exactly
3. Ensure OAuth app is enabled
4. Try incognito/private browsing mode

### Search not working

1. Verify `search-index.js` exists in `/web/js/`
2. Run `python scripts/generate-search-index.py`
3. Clear browser cache
4. Check browser console for errors

### Workflows not running

1. Go to **Actions** tab
2. Find workflow and click **Enable workflow**
3. Check workflow permissions in Settings → Actions
4. Verify schedule in workflow YAML file

### FBI Vault fetch failing

1. Check internet connection
2. Verify FBI Vault URLs are accessible
3. Check disk space (need ~500MB)
4. Review logs in Actions tab

---

## Cost Breakdown

| Service | Cost | What's Included |
|---------|------|-----------------|
| **GitHub Pages** | $0 | Unlimited public repos, SSL, CDN |
| **GitHub Actions** | $0 | 2,000 minutes/month (plenty for our workflows) |
| **GitHub OAuth** | $0 | Unlimited authentications |
| **Wikipedia API** | $0 | Unlimited requests |
| **Lunr.js** | $0 | Client-side search library |
| **Storage** | $0 | 1GB repo + 1GB Git LFS |
| **Cloudflare CDN** | $0 | Optional, 100GB bandwidth |
| **Custom Domain** | $0-50/year | Optional |
| **TOTAL** | **$0/month** | **Everything included!** |

**Annual savings: $15,720-16,320** compared to Azure full production

---

## Support

### Documentation
- **FREE Tier Setup:** `docs/FREE_TIER_SETUP.md`
- **Staff Portal Guide:** `docs/STAFF_PORTAL_GUIDE.md`
- **Access Control Setup:** `docs/ACCESS_CONTROL_SETUP.md`
- **Public Files Integration:** `docs/PUBLIC_FILES_INTEGRATION.md`
- **Task Assignment & Calendar:** `docs/STAFF_TASKS_AND_CALENDAR_GUIDE.md`
- **Bot Usage Guide:** `docs/Bot-Usage-Guide.md` (26 AI agents)
- **Deployment Guide:** `docs/DEPLOYMENT_GUIDE.md`

### Getting Help
- GitHub Issues for bugs
- GitHub Discussions for questions
- Pull requests for contributions

---

## Next Steps

1. ✅ Deploy site (Settings → Pages)
2. ✅ Enable branch protection (Settings → Branches)
3. ✅ Set up staff portal (run scripts)
4. ✅ Integrate public files (run fetch scripts)
5. ✅ Enable automated workflows (Actions tab)
6. ✅ Add staff members (Admin panel)
7. ✅ Review volunteer applications (Issues tab)
8. ✅ Monitor AI agents (Staff portal)

---

**🎉 Your Epstein Files Hub is now live at:**
`https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/`

**Monthly cost: $0 | Annual savings: $15,720+ | Production-ready infrastructure**

**Maintained by 26 AI agents | Owner-controlled | Ready to use**
