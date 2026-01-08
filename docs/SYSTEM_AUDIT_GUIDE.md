# System-Wide Military Audit and Inspection Guide

## Overview

The System-Wide Military Audit and Inspection system provides comprehensive automated auditing capabilities for the entire Epstein Files Hub infrastructure. This system performs thorough inspections of all components, generates detailed reports, and provides actionable recommendations for system maintenance and improvement.

## Table of Contents

1. [Introduction](#introduction)
2. [Audit Capabilities](#audit-capabilities)
3. [Quick Start](#quick-start)
4. [Usage Guide](#usage-guide)
5. [Report Formats](#report-formats)
6. [Status Levels](#status-levels)
7. [Automation](#automation)
8. [Integration](#integration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Introduction

### Purpose

The audit system is designed to:
- **Monitor** all infrastructure components continuously
- **Detect** issues early before they become critical
- **Report** findings in military-style formatted reports
- **Recommend** corrective actions
- **Track** system health over time
- **Ensure** compliance with security and quality standards

### Key Features

- ✅ **9 Comprehensive Audit Sections**
- ✅ **Multiple Report Formats** (Markdown, JSON, Text)
- ✅ **Automated Scheduling** (Daily/Weekly)
- ✅ **GitHub Actions Integration**
- ✅ **Issue Creation** for critical findings
- ✅ **Historical Tracking** via logs
- ✅ **Zero External Dependencies** (uses Python stdlib)
- ✅ **Military-Grade Formatting** for professional reports

## Audit Capabilities

### 1. Infrastructure Audit

Validates core infrastructure components:

- **Directory Structure**
  - 12 critical directories verified
  - Existence and write permissions checked
  - Missing directories flagged

- **Configuration Files**
  - 7 essential configuration files
  - Readability verification
  - Missing files reported

- **Python Environment**
  - Version compatibility (3.8+)
  - Package availability
  - Installation verification

- **Git Repository**
  - Status checking
  - Uncommitted changes detection
  - Repository health

### 2. Agent Infrastructure Audit

Monitors all AI agents:

- **Agent Directory Verification**
  - 26+ agent directories checked
  - Documentation completeness
  - Operational status

- **Agent Types Monitored**
  - indexing-bot
  - image-analysis-bot
  - verification-bot
  - search-bot
  - summarization-bot
  - pdf-analysis-bot
  - cross-reference-bot
  - entity-extraction-bot
  - timeline-bot
  - fact-checking-bot
  - audit-bot (self-monitoring)

- **Infrastructure Documentation**
  - AGENT_INFRASTRUCTURE.md presence
  - Bot usage guides
  - Development documentation

### 3. Data Integrity Audit

Validates data storage:

- **Data Directories**
  - data/
  - data/public_files/
  - data/processed/
  - data/wikipedia/

- **Metrics Tracked**
  - File counts
  - Storage size (MB/GB)
  - Directory accessibility
  - Data completeness

### 4. Documentation Audit

Ensures documentation completeness:

- **Required Documents**
  - README.md - Project overview
  - CONTRIBUTING.md - Contribution guidelines
  - SETUP_GUIDE.md - Setup instructions
  - docs/Glossary.md - Terminology
  - docs/CharacterDirectory.md - Character index
  - docs/Timeline.md - Event timeline
  - docs/Bot-Usage-Guide.md - Bot documentation

- **Quality Checks**
  - File existence
  - Minimum size requirements
  - Content validation

### 5. Security Audit

Security compliance verification:

- **Environment Protection**
  - .env file detection (should NOT exist in repo)
  - .env.example template verification
  - Environment variable security

- **Git Security**
  - .gitignore configuration
  - Sensitive file protection
  - Secret management verification

- **Sensitive Files Detection**
  - *.key files
  - *.pem certificates
  - *.p12 keystores
  - Password/secret files

### 6. Workflow Audit

GitHub Actions verification:

- **Workflow Files**
  - .github/workflows/*.yml
  - Configuration validity
  - Scheduling verification

- **Key Workflows**
  - agent-monitoring.yml
  - verify-setup.yml
  - deploy-pages.yml
  - system-audit.yml (self)

### 7. Scripts Audit

Python scripts validation:

- **Script Directory**
  - scripts/*.py files
  - Executable permissions
  - Size and integrity

- **Critical Scripts**
  - fetch-public-files.py
  - fetch-wikipedia-data.py
  - generate-search-index.py
  - process-pdfs.py
  - safe-source-expander.py
  - system-audit.py (self)

### 8. Web Interface Audit

Web assets verification:

- **Files Checked**
  - HTML pages
  - JavaScript files
  - CSS stylesheets
  - Images and assets

- **Metrics**
  - File counts
  - Directory structure
  - Asset accessibility

### 9. Resource Utilization Audit

Resource monitoring:

- **Repository Size**
  - Total files
  - Total size (MB/GB)
  - Growth tracking

- **Log Directory**
  - Size monitoring
  - Cleanup recommendations
  - Warning thresholds

- **Cache Directory**
  - Cache size
  - Optimization suggestions
  - Space management

## Quick Start

### Command Line

```bash
# Run basic audit with markdown report
make system-audit

# Run audit with all report formats
make system-audit-all

# Run military-style audit (alias)
make military-audit

# Run audit quietly (no console output)
make system-audit-quiet

# Direct Python execution
python scripts/system-audit.py

# With custom options
python scripts/system-audit.py --format all --output-dir logs
```

### GitHub Actions

Trigger manually:
1. Go to **Actions** tab
2. Select **System-Wide Audit and Inspection**
3. Click **Run workflow**
4. Choose options and run

## Usage Guide

### Basic Execution

```bash
# Standard audit
python scripts/system-audit.py

# Options:
#   --output-dir DIR    Where to save reports (default: logs)
#   --format FORMAT     Report format: markdown, json, text, all
#   --quiet             Suppress console output
```

### Output Examples

#### Console Output

```
================================================================================
SYSTEM-WIDE MILITARY AUDIT AND INSPECTION
================================================================================
Audit ID: AUDIT-20260104180000
Timestamp: 2026-01-04 18:00:00 UTC
================================================================================

[1/9] INFRASTRUCTURE AUDIT
--------------------------------------------------------------------------------
Status: OPERATIONAL
Issues Found: 0

[2/9] AGENT INFRASTRUCTURE AUDIT
--------------------------------------------------------------------------------
Status: OPERATIONAL
Agents Operational: 10/10

[3/9] DATA INTEGRITY AUDIT
--------------------------------------------------------------------------------
Status: OPERATIONAL
Data Directories: 4/4

...

================================================================================
AUDIT COMPLETE
================================================================================
Audit ID: AUDIT-20260104180000
Overall Status: OPERATIONAL
Issues Found: 0
Recommendations: 3
================================================================================
```

### Report Files

After execution, find reports in `logs/`:

```
logs/
├── system_audit_20260104_180000.md      # Markdown report
├── system_audit_20260104_180000.json    # JSON data
└── system_audit_20260104_180000.txt     # Plain text report
```

## Report Formats

### Markdown Report

Professional formatted report with:
- Executive summary
- Section-by-section findings
- Issues and recommendations
- Audit certification footer

**Use case:** GitHub Issues, documentation, sharing

### JSON Report

Machine-readable structured data:
```json
{
  "audit_id": "AUDIT-20260104180000",
  "timestamp": "2026-01-04T18:00:00Z",
  "overall_status": "OPERATIONAL",
  "sections": {...},
  "summary": {...}
}
```

**Use case:** Automation, dashboards, monitoring systems

### Text Report

Plain text formatted for:
- Email distribution
- Terminal viewing
- Legacy systems

**Use case:** Email alerts, simple viewing

## Status Levels

### OPERATIONAL ✅
- **Meaning:** All systems functioning normally
- **Action:** None required - routine monitoring
- **Color Code:** Green
- **Exit Code:** 0

### WARNING ⚠️
- **Meaning:** Minor issues detected
- **Action:** Review recommendations
- **Color Code:** Yellow
- **Exit Code:** 0

### DEGRADED 🔶
- **Meaning:** Significant issues affecting functionality
- **Action:** Immediate attention needed
- **Color Code:** Orange
- **Exit Code:** 1
- **Triggers:** GitHub Issue creation

### CRITICAL 🚨
- **Meaning:** Severe issues compromising system
- **Action:** Emergency response required
- **Color Code:** Red
- **Exit Code:** 2
- **Triggers:** GitHub Issue with priority labels

## Automation

### Daily Audits

Automatically run every day at 6:00 AM UTC:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily
```

**Actions:**
1. Run full system audit
2. Generate all report formats
3. Commit reports to repository
4. Create issues for DEGRADED/CRITICAL status

### Weekly Deep Audits

Every Sunday at 6:00 AM UTC:

```yaml
schedule:
  - cron: '0 6 * * 0'  # Weekly on Sunday
```

**Additional checks:**
- Git activity analysis
- Repository statistics
- Disk usage trends
- Performance metrics

**Output:**
- Comprehensive weekly summary issue
- Historical trend analysis
- Capacity planning recommendations

### Manual Triggers

Run on-demand via GitHub Actions:
1. Navigate to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Choose audit type:
   - **standard** - Regular audit
   - **deep** - Extended analysis
   - **security-only** - Security focus

## Integration

### Makefile

```bash
# Already integrated commands
make system-audit           # Standard audit
make system-audit-all       # All formats
make military-audit         # Alias
make audit-report           # Alias
```

### Python API

```python
from scripts.system_audit import SystemAuditor

# Create instance
auditor = SystemAuditor()

# Run audit
results = auditor.run_full_audit()

# Get status
overall_status = results['overall_status']
total_issues = results['summary']['total_issues']

# Generate report
markdown_report = auditor.generate_report('markdown')
json_report = auditor.generate_report('json')

# Save reports
auditor.save_report(output_dir='logs', format_type='all')
```

### CI/CD Pipeline

Integrate into existing workflows:

```yaml
- name: Run System Audit
  run: python scripts/system-audit.py --format json
  
- name: Check Audit Status
  run: |
    STATUS=$(python -c "import json; print(json.load(open('logs/system_audit_latest.json'))['overall_status'])")
    if [ "$STATUS" = "CRITICAL" ]; then
      exit 1
    fi
```

## Best Practices

### Regular Monitoring

1. **Review daily audit reports** - Check GitHub for issues created
2. **Track trends** - Monitor recurring recommendations
3. **Address issues promptly** - Fix DEGRADED status items quickly
4. **Plan capacity** - Use weekly reports for planning

### Issue Management

1. **Critical Issues** - Address immediately (same day)
2. **Degraded Status** - Fix within 48 hours
3. **Warnings** - Review weekly
4. **Recommendations** - Implement during maintenance windows

### Report Retention

- **Daily reports:** 90 days
- **Weekly reports:** 1 year
- **Critical incidents:** Indefinite

### Threshold Management

Adjust as system grows:
```python
# In system-audit.py
REPO_SIZE_WARNING = 50  # GB
LOGS_SIZE_WARNING = 1000  # MB
CACHE_SIZE_WARNING = 5000  # MB
```

## Troubleshooting

### Permission Errors

```bash
# Fix permissions
chmod -R u+w logs/
chmod +x scripts/system-audit.py
```

### Module Import Errors

```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use absolute imports
python -m scripts.system-audit
```

### Git Errors

```bash
# Ensure git is configured
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Large Repository Size

```bash
# Clean cache and logs
make clean

# Or specific cleanup
rm -rf cache/*
rm -rf logs/system_audit_*.{md,json,txt}
```

### Audit Takes Too Long

```bash
# Use quiet mode
python scripts/system-audit.py --quiet

# Or run specific sections (modify script)
```

## Advanced Usage

### Custom Audit Sections

Add new sections by extending `SystemAuditor`:

```python
def _audit_custom_section(self):
    section = {
        "status": "OPERATIONAL",
        "checks": {},
        "issues": [],
        "recommendations": []
    }
    
    # Your checks here
    
    self.audit_results["sections"]["custom"] = section
```

### Threshold Customization

```python
# Create custom auditor
class CustomAuditor(SystemAuditor):
    REPO_SIZE_THRESHOLD = 100  # GB
    LOGS_SIZE_THRESHOLD = 2000  # MB
```

### Integration with Monitoring Systems

Export metrics:
```bash
# Generate JSON for monitoring
python scripts/system-audit.py --format json --quiet

# Parse and send to monitoring
python scripts/send-to-monitoring.py logs/system_audit_latest.json
```

## Related Documentation

- [bots/audit-bot/README.md](../bots/audit-bot/README.md) - Audit bot details
- [bots/AGENT_INFRASTRUCTURE.md](../bots/AGENT_INFRASTRUCTURE.md) - Agent system
- [.github/workflows/system-audit.yml](../.github/workflows/system-audit.yml) - Workflow config
- [Makefile](../Makefile) - Available commands

## Support

For issues or questions:
- **GitHub Issues:** Use label `audit` or `audit-bot`
- **Documentation:** Check related docs above
- **Logs:** Review `logs/system_audit_*.{md,json,txt}`

## Changelog

### Version 1.0.0 (2026-01-04)
- ✅ Initial release
- ✅ 9 comprehensive audit sections
- ✅ Multiple report formats
- ✅ GitHub Actions integration
- ✅ Automated daily/weekly audits
- ✅ Issue creation for critical status

---

**Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** System Audit Bot
**Status:** ✅ Production Ready
