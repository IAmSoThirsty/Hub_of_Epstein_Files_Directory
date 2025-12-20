# Access Control Setup Guide

## Overview

This guide explains how to configure repository access controls to ensure only the owner (`@IAmSoThirsty`) can directly modify the site while allowing volunteers to contribute through a controlled, review-based process.

---

## Quick Setup Checklist

- [ ] Enable branch protection rules
- [ ] Add CODEOWNERS file (already created)
- [ ] Configure required reviews
- [ ] Enable status checks
- [ ] Restrict push access
- [ ] Enable volunteer application workflow (optional)
- [ ] Test access controls

**Time Required:** 10-15 minutes  
**Difficulty:** Easy  
**Cost:** $0 (all GitHub free features)

---

## Step 1: Enable Branch Protection Rules

Branch protection ensures no one can push directly to the main branch without review and approval.

### 1.1 Navigate to Settings

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Branches** in left sidebar

### 1.2 Add Branch Protection Rule

1. Click **Add rule** button
2. In **Branch name pattern**, enter: `main`

### 1.3 Configure Protection Rules

Check the following options:

#### Require Pull Request Reviews
- ✅ **Require a pull request before merging**
  - ✅ **Require approvals:** Set to **1**
  - ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - ✅ **Require review from Code Owners**
  - ✅ **Restrict who can dismiss pull request reviews**
    - Select: **IAmSoThirsty** (your username)

#### Require Status Checks
- ✅ **Require status checks to pass before merging**
  - ✅ **Require branches to be up to date before merging**

#### Additional Restrictions
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (optional, recommended)
- ✅ **Include administrators** (important!)
- ✅ **Restrict who can push to matching branches**
  - Select: **IAmSoThirsty** (your username)
- ✅ **Allow force pushes:** **OFF**
- ✅ **Allow deletions:** **OFF**

### 1.4 Save Protection Rule

1. Scroll to bottom
2. Click **Create** button
3. Confirm settings

**Result:** Main branch is now protected. Only you can push directly.

---

## Step 2: Verify CODEOWNERS File

The CODEOWNERS file is already created in `.github/CODEOWNERS`. It ensures all pull requests automatically request your review.

### 2.1 Verify File Exists

```bash
cat .github/CODEOWNERS
```

Should show:
```
# All files require owner review
* @IAmSoThirsty

# Critical infrastructure files
/.github/ @IAmSoThirsty
/.github/workflows/ @IAmSoThirsty
/scripts/ @IAmSoThirsty
/bots/ @IAmSoThirsty
/docs/ @IAmSoThirsty
/data/ @IAmSoThirsty
/web/ @IAmSoThirsty

# Configuration files
*.yml @IAmSoThirsty
*.yaml @IAmSoThirsty
*.json @IAmSoThirsty
*.md @IAmSoThirsty
```

### 2.2 Commit CODEOWNERS (if needed)

If the file doesn't exist yet:
```bash
git add .github/CODEOWNERS
git commit -m "Add CODEOWNERS for access control"
git push
```

**Result:** All PRs now automatically request your review.

---

## Step 3: Configure Required Status Checks (Optional)

Set up automated checks that must pass before PRs can be merged.

### 3.1 Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Select: **Allow all actions and reusable workflows**
3. Scroll down to **Workflow permissions**
4. Select: **Read repository contents and packages permissions**
5. ✅ **Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

### 3.2 Add Status Check Requirements

1. Go to **Settings** → **Branches**
2. Click **Edit** on your main branch protection rule
3. Scroll to **Require status checks to pass before merging**
4. Search and select checks to require:
   - `volunteer-application` (if using volunteer system)
   - `update-search-index` (if auto-generating index)
   - Any other workflows you want to require
5. Click **Save changes**

**Result:** PRs must pass automated checks before merging.

---

## Step 4: Restrict Collaborator Permissions

Control who can be added as collaborators and what they can do.

### 4.1 Review Current Collaborators

1. Go to **Settings** → **Collaborators**
2. Review list of collaborators
3. Remove anyone who shouldn't have access

### 4.2 Set Base Permissions

1. Go to **Settings** → **Collaborators and teams**
2. Under **Manage access**, verify:
   - **Base permissions:** **No permission**
   - This means new collaborators get no access by default

### 4.3 Invite Policy (if needed)

When adding volunteers as collaborators:
1. Click **Add people**
2. Enter their GitHub username
3. Select role:
   - **Read** for Level 2 (Viewer)
   - **Triage** for Level 3 (Contributor)
   - **Write** for Level 4 (Editor) - but PRs still required
4. Click **Add to repository**

**Note:** With branch protection, even "Write" access can't bypass PR requirements.

**Result:** You control all access explicitly.

---

## Step 5: Enable Volunteer Application Workflow (Optional)

If you want to accept volunteer applications through the web form.

### 5.1 Enable Workflow

1. Go to **Actions** tab
2. Find **Volunteer Application Handler**
3. Click **Enable workflow**

### 5.2 Create Personal Access Token (if needed)

The workflow needs a token to create/update issues:

1. Click your profile picture → **Settings**
2. Scroll to **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **Generate new token** → **Generate new token (classic)**
4. Set:
   - **Note:** "Volunteer Management Bot"
   - **Expiration:** 90 days or custom
   - **Scopes:**
     - ✅ `repo` (full control)
     - ✅ `workflow`
5. Click **Generate token**
6. **Copy the token** (you won't see it again)

### 5.3 Add Token to Repository Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `VOLUNTEER_BOT_TOKEN`
4. Value: Paste your token
5. Click **Add secret**

### 5.4 Test Workflow

1. Visit your site's volunteer page
2. Submit a test application
3. Check if GitHub Issue is created
4. Comment `approve: level-3` on the issue
5. Verify bot responds with instructions

**Result:** Volunteer applications automated.

---

## Step 6: Test Access Controls

Verify everything works as expected.

### 6.1 Test Direct Push (Should Fail)

From another account or computer:
```bash
git clone https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory
echo "test" > test.txt
git add test.txt
git commit -m "Test"
git push
```

**Expected Result:** Push rejected with message about branch protection.

### 6.2 Test Pull Request (Should Work)

1. Fork repository (from another account)
2. Make changes
3. Create pull request
4. Verify:
   - You're automatically requested as reviewer
   - Cannot merge without your approval
   - All status checks must pass

### 6.3 Test Owner Push (Should Work)

From your account:
```bash
# You can push directly
echo "# Access Control Verified" > test.txt
git add test.txt
git commit -m "Test owner access"
git push
```

**Expected Result:** Push succeeds (you're the owner).

**Result:** Access controls working correctly.

---

## Step 7: Document Your Policies

Create clear documentation for volunteers.

### 7.1 Update README

Add section about access control:
```markdown
## Access Control

This repository uses strict access controls:
- Only the owner can directly commit to main branch
- All volunteer changes require pull request review
- Owner approval required for all merges
- See [Volunteer Management Guide](docs/VOLUNTEER_MANAGEMENT.md)
```

### 7.2 Update CONTRIBUTING.md

Ensure it explains the PR workflow clearly.

### 7.3 Add to Volunteer Page

The volunteer.html page already explains the process.

**Result:** Clear expectations for contributors.

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review open pull requests
- Check volunteer activity
- Process new applications

**Monthly:**
- Review collaborator list
- Check activity reports
- Update permissions if needed

**Quarterly:**
- Review branch protection rules
- Update CODEOWNERS if needed
- Rotate personal access tokens

### Monitoring

**Watch For:**
- Unauthorized access attempts
- Quality issues in PRs
- Slow response times from volunteers
- Repeated violations of guidelines

**Tools:**
- GitHub Insights → Pulse
- GitHub Insights → Contributors
- Actions → Workflow runs
- Settings → Audit log

---

## Troubleshooting

### Problem: Can't Push to Main

**Cause:** Branch protection is working correctly.

**Solution:** Create a PR instead, or temporarily disable protection (not recommended).

### Problem: PR Can't Be Merged

**Cause:** Missing required reviews or failing status checks.

**Solution:** 
1. Review and approve the PR
2. Ensure all checks pass
3. Resolve any conflicts
4. Then merge

### Problem: CODEOWNERS Not Working

**Cause:** File not in .github/ or incorrect format.

**Solution:**
1. Verify file location: `.github/CODEOWNERS`
2. Check syntax (no empty lines between entries)
3. Ensure usernames start with @
4. Commit and push changes

### Problem: Workflow Not Running

**Cause:** Workflow disabled or permissions issue.

**Solution:**
1. Go to Actions → Find workflow → Enable
2. Check workflow file syntax
3. Verify repository secrets
4. Check Actions permissions in Settings

### Problem: Volunteer Can't Fork

**Cause:** Repository visibility settings.

**Solution:**
1. Ensure repository is public
2. Check organization settings (if applicable)
3. Verify volunteer's GitHub account is active

---

## Advanced Configuration

### Protected Branches (Multiple)

To protect additional branches:
```
develop   # Development branch
staging   # Staging branch
release/* # Release branches
```

Follow same steps as main branch protection.

### Required Checks

Add more sophisticated checks:
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks
on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for sources
        run: |
          # Verify PR includes source citations
          python scripts/validate-sources.py
```

### Auto-Assignment

Automatically assign PRs to owner:
```yaml
# .github/auto-assign.yml
addReviewers: true
addAssignees: true
reviewers:
  - IAmSoThirsty
assignees:
  - IAmSoThirsty
numberOfReviewers: 1
```

---

## Security Best Practices

### Secrets Management
- ✅ Never commit secrets to repository
- ✅ Use repository secrets for tokens
- ✅ Rotate tokens regularly (every 90 days)
- ✅ Use minimal required permissions
- ❌ Don't share tokens with volunteers

### Code Review
- ✅ Review every line of volunteer code
- ✅ Check for malicious patterns
- ✅ Verify source citations
- ✅ Test changes locally before merging
- ❌ Don't merge without thorough review

### Access Control
- ✅ Minimum necessary permissions
- ✅ Regular access audits
- ✅ Remove inactive collaborators
- ✅ Monitor audit logs
- ❌ Don't give admin access to volunteers

---

## FAQ

### Q: Can I temporarily disable branch protection?
**A:** Yes, but not recommended. Edit the rule and uncheck "Include administrators" if you must bypass temporarily. Re-enable immediately after.

### Q: What if I accidentally merge a bad PR?
**A:** Revert the merge:
```bash
git revert -m 1 <merge-commit-hash>
git push
```

### Q: Can volunteers see my personal access token?
**A:** No, repository secrets are encrypted and not visible to anyone except you and GitHub Actions.

### Q: How do I remove a volunteer's access?
**A:** Go to Settings → Collaborators → Find their name → Remove.

### Q: What if a volunteer tries to bypass protections?
**A:** Branch protection prevents this. If they attempt unauthorized access, revoke their access immediately and document the incident.

---

## Checklist Summary

- [ ] Branch protection enabled on main
- [ ] CODEOWNERS file added
- [ ] Required reviews configured
- [ ] Push restrictions set (owner only)
- [ ] Workflow permissions configured
- [ ] Volunteer application workflow enabled (optional)
- [ ] Personal access token created (if using workflows)
- [ ] Token added to repository secrets
- [ ] Access controls tested
- [ ] Documentation updated
- [ ] Policies communicated to volunteers

---

## Support

### Getting Help
- **GitHub Docs:** https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository
- **Branch Protection:** https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches
- **CODEOWNERS:** https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

### Contact
- **Issues:** https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory/issues
- **Discussions:** https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory/discussions

---

**Your repository is now secure with owner-only control while enabling safe volunteer contributions!**
