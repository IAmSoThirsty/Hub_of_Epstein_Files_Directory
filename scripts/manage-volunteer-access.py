#!/usr/bin/env python3
"""
Volunteer Access Management Script
Handles volunteer application processing and access control
"""

import os
import re
import json
from datetime import datetime

def parse_application(issue_body):
    """Parse volunteer application from GitHub issue body"""
    application = {}
    
    # Extract key information
    name_match = re.search(r'\*\*Full Name:\*\*\s*(.+)', issue_body)
    email_match = re.search(r'\*\*Email:\*\*\s*(.+)', issue_body)
    github_match = re.search(r'\*\*GitHub Username:\*\*\s*(.+)', issue_body)
    role_match = re.search(r'\*\*Desired Role:\*\*\s*(.+)', issue_body)
    experience_match = re.search(r'\*\*Experience Level:\*\*\s*(.+)', issue_body)
    
    if name_match:
        application['name'] = name_match.group(1).strip()
    if email_match:
        application['email'] = email_match.group(1).strip()
    if github_match:
        application['github_username'] = github_match.group(1).strip().replace('@', '')
    if role_match:
        application['role'] = role_match.group(1).strip()
    if experience_match:
        application['experience'] = experience_match.group(1).strip()
    
    return application

def get_permission_level(comment_body):
    """Extract permission level from owner's approval comment"""
    # Look for "approve: level-X" pattern
    approve_match = re.search(r'approve:\s*level-(\d)', comment_body, re.IGNORECASE)
    if approve_match:
        return int(approve_match.group(1))
    return None

def generate_access_instructions(level, github_username):
    """Generate instructions for setting up volunteer access"""
    instructions = {
        2: f"""
## Access Approved: Level 2 (Viewer)

@{github_username} has been approved as a **Viewer**.

**Permissions:**
- ✅ Read access to all public documentation
- ✅ View search interface
- ✅ Browse character profiles and locations
- ❌ No ability to submit changes

**No further setup required.** Access is already available through the public GitHub Pages site.

**Resources:**
- Site: https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/
- Documentation: [Volunteer Management Guide](docs/VOLUNTEER_MANAGEMENT.md)
""",
        3: f"""
## Access Approved: Level 3 (Contributor)

@{github_username} has been approved as a **Contributor**.

**Permissions:**
- ✅ Fork repository
- ✅ Submit pull requests
- ✅ Suggest document additions
- ✅ Propose corrections
- ❌ Cannot merge own PRs (requires owner approval)

**Setup Instructions:**

1. **Fork the repository:**
   - Go to https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory
   - Click "Fork" button

2. **Clone your fork:**
   ```bash
   git clone https://github.com/{github_username}/Hub_of_Epstein_Files_Directory.git
   cd Hub_of_Epstein_Files_Directory
   ```

3. **Make changes in a new branch:**
   ```bash
   git checkout -b add-new-document
   # Make your changes
   git add .
   git commit -m "Add: Brief description"
   git push origin add-new-document
   ```

4. **Submit Pull Request:**
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Fill out the PR template completely
   - Wait for owner review

**Guidelines:**
- All changes must go through pull requests
- Provide sources for new information
- Follow the PR template
- Respond to review feedback promptly
- Owner approval required for all merges

**Resources:**
- [Volunteer Management Guide](docs/VOLUNTEER_MANAGEMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [PR Template](.github/PULL_REQUEST_TEMPLATE.md)
""",
        4: f"""
## Access Approved: Level 4 (Editor)

@{github_username} has been approved as an **Editor**.

**Permissions:**
- ✅ Fork repository
- ✅ Submit pull requests with broader changes
- ✅ Edit multiple documents
- ✅ Process uploaded PDFs
- ✅ Tag and categorize content
- ❌ Cannot merge own PRs (requires owner approval)
- ❌ Cannot modify workflows or configurations

**Setup Instructions:**

1. **Fork the repository:**
   - Go to https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory
   - Click "Fork" button

2. **Clone your fork:**
   ```bash
   git clone https://github.com/{github_username}/Hub_of_Epstein_Files_Directory.git
   cd Hub_of_Epstein_Files_Directory
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make changes in a new branch:**
   ```bash
   git checkout -b update-character-profiles
   # Make your changes
   # Run processing scripts if needed
   python scripts/process-pdfs.py
   python scripts/generate-search-index.py
   git add .
   git commit -m "Update: Brief description"
   git push origin update-character-profiles
   ```

5. **Submit Pull Request:**
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Fill out the PR template completely
   - Wait for owner review

**Additional Responsibilities:**
- Process uploaded documents promptly
- Maintain data quality standards
- Document all changes clearly
- Respond to owner feedback
- Follow coding standards

**Guidelines:**
- All changes must go through pull requests
- Provide comprehensive sources
- Test changes locally before submitting
- Follow the PR template meticulously
- Owner approval required for all merges
- Do NOT modify .github/workflows/ or scripts/ without explicit permission

**Resources:**
- [Volunteer Management Guide](docs/VOLUNTEER_MANAGEMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Scripts Documentation](scripts/README.md)
- [Bot Usage Guide](docs/Bot-Usage-Guide.md)
"""
    }
    
    return instructions.get(level, "Invalid permission level")

def main():
    """Main execution function"""
    issue_number = os.getenv('ISSUE_NUMBER')
    issue_body = os.getenv('ISSUE_BODY')
    comment_body = os.getenv('COMMENT_BODY', '')
    
    if not issue_body and not comment_body:
        print("No issue or comment body found")
        return
    
    # If this is a new application (issue opened)
    if issue_body and 'Volunteer Application' in issue_body:
        application = parse_application(issue_body)
        print(f"Application received from: {application.get('name', 'Unknown')}")
        print(f"Role requested: {application.get('role', 'Unknown')}")
        print(f"GitHub: @{application.get('github_username', 'Unknown')}")
        
        # Log application
        log_file = 'data/volunteer_applications.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                applications = json.load(f)
        else:
            applications = []
        
        applications.append({
            **application,
            'issue_number': issue_number,
            'date': datetime.now().isoformat(),
            'status': 'pending'
        })
        
        os.makedirs('data', exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(applications, f, indent=2)
        
        print(f"Application logged. Awaiting owner review.")
    
    # If this is an approval comment
    if comment_body:
        level = get_permission_level(comment_body)
        if level:
            # Extract GitHub username from issue
            if issue_body:
                application = parse_application(issue_body)
                github_username = application.get('github_username', 'unknown')
                
                instructions = generate_access_instructions(level, github_username)
                print(instructions)
                
                # Update application status
                log_file = 'data/volunteer_applications.json'
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        applications = json.load(f)
                    
                    for app in applications:
                        if app.get('issue_number') == issue_number:
                            app['status'] = f'approved-level-{level}'
                            app['approved_date'] = datetime.now().isoformat()
                            break
                    
                    with open(log_file, 'w') as f:
                        json.dump(applications, f, indent=2)
                
                print(f"Access approved at Level {level} for @{github_username}")

if __name__ == '__main__':
    main()
