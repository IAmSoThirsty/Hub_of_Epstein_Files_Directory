# Volunteer Management Guide

## Overview

This document explains the volunteer management system for the Epstein Files Hub. The system is designed to allow the repository owner (`@IAmSoThirsty`) to maintain complete control over all modifications while enabling trusted volunteers to contribute safely through a structured, permission-based workflow.

## Key Principles

### 1. Owner-Only Control
- **Only the repository owner** can directly commit to the main branch
- **Only the owner** can merge pull requests
- **Only the owner** can modify workflows, configurations, and critical infrastructure
- **Owner approval required** for all changes

### 2. Volunteer Contributions
- Volunteers work through **pull requests only**
- All changes reviewed and approved by owner
- Strict permission levels enforce capabilities
- Activity monitored and reported

### 3. Security & Quality
- Branch protection prevents unauthorized changes
- CODEOWNERS file enforces owner review
- All new information requires source citations
- Background checks for sensitive roles (optional)

---

## Permission Levels

### Level 1: Applicant
**Status:** Application submitted, pending review

**Access:**
- None - awaiting owner decision

**Process:**
1. Submit application via volunteer.html
2. GitHub Issue created automatically
3. Owner reviews application
4. Owner approves or rejects

---

### Level 2: Viewer
**Status:** Read-only access

**Permissions:**
- ✅ View all public documentation
- ✅ Access search interface
- ✅ Browse character profiles
- ✅ View location guides
- ✅ Read timelines and sources
- ❌ Cannot submit changes
- ❌ Cannot fork repository

**Use Case:**
- Learning about the project
- Researching information
- Evaluating before contributing

**No Setup Required:**
Simply visit the public GitHub Pages site.

---

### Level 3: Contributor
**Status:** Can submit pull requests

**Permissions:**
- ✅ Fork repository
- ✅ Submit pull requests
- ✅ Add new documents
- ✅ Suggest corrections
- ✅ Propose new content
- ❌ Cannot merge PRs (owner only)
- ❌ Cannot modify workflows
- ❌ Cannot change configurations

**Workflow:**
1. Fork repository
2. Make changes in feature branch
3. Submit pull request
4. Owner reviews and provides feedback
5. Make requested changes
6. Owner approves and merges

**Responsibilities:**
- Provide accurate sources for all new information
- Follow contribution guidelines
- Respond to review feedback promptly
- Maintain professionalism
- Follow coding/documentation standards

**Setup:**
```bash
# Fork repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# Create feature branch
git checkout -b add-new-document

# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Add: Brief description"
git push origin add-new-document

# Open pull request on GitHub
```

---

### Level 4: Editor
**Status:** Can make broader edits via PRs

**Permissions:**
- ✅ Fork repository
- ✅ Submit pull requests with multiple file changes
- ✅ Edit character profiles
- ✅ Update timeline entries
- ✅ Process uploaded PDFs
- ✅ Tag and categorize content
- ✅ Run processing scripts
- ❌ Cannot merge PRs (owner only)
- ❌ Cannot modify workflows without permission
- ❌ Cannot change core configurations

**Workflow:**
1. Fork repository
2. Make changes in feature branch
3. Run processing scripts if needed
4. Test changes locally
5. Submit pull request with comprehensive description
6. Owner reviews thoroughly
7. Address feedback
8. Owner approves and merges

**Responsibilities:**
- Process uploaded documents promptly
- Maintain data quality standards
- Document all changes clearly
- Test changes before submitting
- Follow coding standards strictly
- Provide comprehensive sources
- Train new contributors (if needed)

**Setup:**
```bash
# Fork repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# Install dependencies
pip install -r requirements.txt

# Create feature branch
git checkout -b update-character-profiles

# Make changes
# ... edit files ...

# Run processing scripts
python scripts/process-pdfs.py
python scripts/generate-search-index.py

# Test locally
cd web
python -m http.server 8000
# Visit http://localhost:8000 to test

# Commit and push
git add .
git commit -m "Update: Brief description"
git push origin update-character-profiles

# Open pull request on GitHub
```

---

### Level 5: Administrator
**Status:** Full repository access

**Permissions:**
- ✅ All capabilities
- ✅ Direct commits to main branch
- ✅ Merge pull requests
- ✅ Modify workflows
- ✅ Change configurations
- ✅ Manage collaborators
- ✅ Access repository secrets

**Who Has This:**
- **Only the repository owner** (`@IAmSoThirsty`)
- **Cannot be granted to volunteers**

---

## Volunteer Application Process

### Step 1: Submit Application

1. Visit: https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/volunteer.html
2. Complete the application form:
   - Full name
   - Email address
   - GitHub username
   - Desired role
   - Experience level
   - Time commitment
   - Motivation
   - Skills/experience
3. Accept all agreements
4. Submit application
5. GitHub Issue created automatically

### Step 2: Owner Reviews Application

The owner reviews:
- Application information
- GitHub profile
- Relevant experience
- Time commitment
- Motivation

**Review Time:** Typically 3-7 days

### Step 3: Owner Decision

The owner comments on the GitHub Issue:

**To Approve:**
```
approve: level-2   # For Viewer
approve: level-3   # For Contributor  
approve: level-4   # For Editor
```

**To Reject:**
```
reject: Insufficient experience with research projects
reject: Unable to commit required time
reject: Not a good fit for current needs
```

### Step 4: Bot Processes Decision

The volunteer application bot automatically:
- Detects owner's decision
- Generates appropriate instructions
- Posts them to the GitHub Issue
- Updates application log
- Notifies applicant

### Step 5: Volunteer Setup

**If Approved:**
- Volunteer receives setup instructions based on level
- Follows onboarding guide
- Gains access as specified
- Can begin contributing

**If Rejected:**
- Volunteer receives explanation
- Can reapply after addressing concerns
- No access granted

---

## Pull Request Review Process

### For Contributors (Level 3)

1. **Volunteer Submits PR:**
   - Uses PR template
   - Describes changes clearly
   - Provides sources
   - Links related issues

2. **Automated Checks:**
   - CODEOWNERS enforces owner review
   - Branch protection checks status
   - No merge until owner approves

3. **Owner Reviews:**
   - Examines changes thoroughly
   - Verifies sources
   - Checks accuracy
   - Tests functionality (if code)
   - Requests changes if needed

4. **Volunteer Responds:**
   - Addresses feedback
   - Makes requested changes
   - Provides clarifications
   - Resubmits for review

5. **Owner Approves:**
   - Final review
   - Approves PR
   - Merges to main branch
   - Closes related issues

### For Editors (Level 4)

Same process, but with additional scrutiny:
- More thorough testing required
- Code review for scripts
- Verification of automated processes
- Impact assessment on search index
- Documentation updates reviewed

---

## Activity Monitoring

### What is Monitored

- All pull requests
- Commit frequency
- Code quality
- Response time to feedback
- Source citation quality
- Adherence to guidelines

### Monthly Reports

The owner receives monthly activity reports:
- Volunteer contribution summary
- Pull requests submitted/merged
- Quality metrics
- Response time statistics
- Recommendations for level changes

### Level Changes

**Promotion:**
- Consistent high-quality contributions
- Fast response to feedback
- Excellent source citations
- Demonstrated responsibility
- Owner discretion

**Demotion:**
- Quality issues
- Slow response to feedback
- Guideline violations
- Inactivity
- Owner discretion

**Access Revocation:**
- Serious violations
- Unauthorized modification attempts
- Providing false information
- Code of conduct violations
- Owner discretion

---

## Access Revocation

### Temporary Suspension

**Reasons:**
- Quality concerns
- Missed deadlines
- Minor guideline violations

**Process:**
1. Owner comments: `suspend: @username reason`
2. Bot removes from collaborators (if applicable)
3. PR permissions retained
4. Review after 30 days

### Permanent Revocation

**Reasons:**
- Serious violations
- Repeated issues after warnings
- Unauthorized access attempts
- False information
- Code of conduct violations

**Process:**
1. Owner comments: `revoke: @username reason`
2. Bot removes all access
3. GitHub blocks applied
4. Application logged
5. Cannot reapply

---

## Best Practices for Volunteers

### Communication
- ✅ Respond to feedback within 48 hours
- ✅ Ask questions if unclear
- ✅ Update on progress regularly
- ✅ Professional and respectful tone
- ❌ Don't argue with owner decisions

### Quality
- ✅ Provide comprehensive sources
- ✅ Verify all information
- ✅ Test changes thoroughly
- ✅ Follow style guidelines
- ❌ Don't submit unverified content

### Workflow
- ✅ One PR per logical change
- ✅ Use descriptive commit messages
- ✅ Keep PRs focused and small
- ✅ Update documentation
- ❌ Don't submit massive PRs

### Security
- ✅ Never share repository secrets
- ✅ Don't expose sensitive data
- ✅ Follow security guidelines
- ✅ Report vulnerabilities privately
- ❌ Don't attempt unauthorized access

---

## Common Questions

### Q: How long does application review take?
**A:** Typically 3-7 days, but can vary based on owner availability.

### Q: Can I apply for multiple roles?
**A:** Choose one primary role. You can expand later based on performance.

### Q: What if my PR is rejected?
**A:** Address the feedback and resubmit. Learn from each review.

### Q: How do I get promoted to Level 4?
**A:** Consistent high-quality contributions at Level 3 over 3+ months.

### Q: Can volunteers become administrators?
**A:** No. Level 5 (Administrator) is reserved for the repository owner only.

### Q: What happens if I become inactive?
**A:** After 90 days of inactivity, access may be reviewed and potentially revoked.

### Q: Can I work on multiple PRs simultaneously?
**A:** Yes, but ensure each is in a separate branch and well-organized.

### Q: How do I report issues with other volunteers?
**A:** Contact the owner directly via GitHub or email.

---

## Technical Setup Guides

### For Contributors (Level 3)

**Git Workflow:**
```bash
# Keep your fork synced
git remote add upstream https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Create feature branch
git checkout -b feature/add-document

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add: Document about X from Y source"

# Push
git push origin feature/add-document

# Open PR on GitHub
```

### For Editors (Level 4)

**Full Setup:**
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install tesseract-ocr poppler-utils

# Or macOS
brew install tesseract poppler

# Test scripts
python scripts/fetch-public-files.py --help
python scripts/process-pdfs.py --help
python scripts/generate-search-index.py --help

# Create feature branch
git checkout -b feature/process-new-documents

# Process documents
python scripts/process-pdfs.py

# Generate search index
python scripts/generate-search-index.py

# Test locally
cd web
python -m http.server 8000
# Visit http://localhost:8000

# Commit and push
git add .
git commit -m "Process: New FBI documents batch 5"
git push origin feature/process-new-documents
```

---

## Support & Resources

### Documentation
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Access Control Setup](ACCESS_CONTROL_SETUP.md)
- [Scripts Documentation](../scripts/README.md)
- [Bot Usage Guide](Bot-Usage-Guide.md)

### Templates
- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)
- [Issue Templates](../.github/ISSUE_TEMPLATE/)

### Contact
- **GitHub Issues:** For questions and discussions
- **Pull Requests:** For code/content contributions
- **Owner:** @IAmSoThirsty

---

## Version History

- **v1.0** (2024-12-20): Initial volunteer management system
- Permission levels defined (1-5)
- Application process established
- PR review workflow documented
- Activity monitoring implemented

---

**Remember:** The repository owner maintains complete control at all times. All volunteer contributions are subject to review and approval. This system ensures quality, security, and accountability while enabling community participation.
