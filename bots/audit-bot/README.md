# System Audit Bot

## Purpose
Performs comprehensive military-style system audits and inspections across the entire infrastructure.

## Features
- **Infrastructure Audit** - Verifies directory structure, configuration files, and core components
- **Agent Health Check** - Monitors all 26+ AI agents and their operational status
- **Data Integrity** - Validates data storage, file counts, and integrity
- **Documentation Review** - Ensures all required documentation is present and complete
- **Security Compliance** - Checks for security vulnerabilities and configuration issues
- **Workflow Status** - Audits GitHub Actions workflows
- **Script Validation** - Verifies all Python scripts are operational
- **Web Interface** - Checks web pages and assets
- **Resource Utilization** - Monitors disk usage and resource consumption

## Configuration

### Bot Settings
```yaml
bot_name: audit-bot
capacity: continuous  # Always available for audits
priority: critical
schedule: daily  # Automated daily audits
manual_trigger: enabled
```

## Usage

### Basic Usage
```bash
# Run full system audit
python scripts/system-audit.py

# Run with markdown output
python scripts/system-audit.py --format markdown

# Run with all formats
python scripts/system-audit.py --format all

# Quiet mode (no console output)
python scripts/system-audit.py --quiet
```

### Command Line Options
```bash
--output-dir DIR    Directory to save reports (default: logs)
--format FORMAT     Report format: markdown, json, text, or all
--quiet             Suppress console output
```

### Makefile Integration
```bash
# Run system audit
make system-audit

# Run audit and generate reports
make audit-report
```

### API Usage
```python
from scripts.system_audit import SystemAuditor

# Create auditor instance
auditor = SystemAuditor()

# Run full audit
results = auditor.run_full_audit()

# Generate report
report = auditor.generate_report(format_type="markdown")

# Save reports
auditor.save_report(output_dir="logs", format_type="all")
```

## Output Format

### Report Sections

1. **Infrastructure Audit**
   - Directory structure verification
   - Configuration file checks
   - Python environment status
   - Git repository status

2. **Agent Infrastructure Audit**
   - All 26+ agents status
   - Agent documentation verification
   - Operational capacity assessment

3. **Data Integrity Audit**
   - Data directory structure
   - File counts and sizes
   - Storage utilization

4. **Documentation Audit**
   - Required documentation presence
   - Document completeness
   - Size and quality checks

5. **Security Audit**
   - Environment variable protection
   - .gitignore configuration
   - Sensitive file detection
   - Security best practices

6. **Workflow Audit**
   - GitHub Actions status
   - Workflow file validation
   - Required workflows check

7. **Scripts Audit**
   - Python scripts validation
   - Script executability
   - Size and integrity checks

8. **Web Interface Audit**
   - HTML pages count
   - JavaScript files
   - CSS stylesheets
   - Asset validation

9. **Resource Utilization Audit**
   - Repository size
   - Logs directory size
   - Cache directory size
   - Resource recommendations

### Sample Output (Markdown)

```markdown
# SYSTEM-WIDE MILITARY AUDIT AND INSPECTION REPORT

---

**Audit ID:** AUDIT-20260104180000
**Timestamp:** 2026-01-04T18:00:00Z
**Classification:** INTERNAL USE
**Overall Status:** OPERATIONAL

---

## EXECUTIVE SUMMARY

- **Total Sections Audited:** 9
- **Total Issues Found:** 2
- **Total Recommendations:** 5
- **System Status:** OPERATIONAL

## INFRASTRUCTURE
**Status:** OPERATIONAL

### Issues
- ⚠️ None

### Recommendations
- 💡 Consider regular backup automation

---

## AUDIT CERTIFICATION

This audit was conducted automatically on 2026-01-04 at 18:00:00 UTC.
All findings are based on automated checks and should be verified by human operators.

**END OF REPORT**
```

### Sample Output (JSON)

```json
{
  "audit_id": "AUDIT-20260104180000",
  "timestamp": "2026-01-04T18:00:00Z",
  "audit_type": "system_wide_inspection",
  "classification": "INTERNAL USE",
  "overall_status": "OPERATIONAL",
  "sections": {
    "infrastructure": {
      "status": "OPERATIONAL",
      "components": {...},
      "issues": [],
      "recommendations": []
    },
    ...
  },
  "summary": {
    "total_sections": 9,
    "total_issues": 2,
    "total_recommendations": 5,
    "overall_status": "OPERATIONAL"
  }
}
```

## Status Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **OPERATIONAL** | All systems functioning normally | None - routine monitoring |
| **WARNING** | Minor issues detected | Review recommendations |
| **DEGRADED** | Significant issues affecting functionality | Immediate attention needed |
| **CRITICAL** | Severe issues compromising system | Emergency response required |

## Audit Sections Detail

### Infrastructure Components
- ✅ Directory structure (12 critical directories)
- ✅ Configuration files (7 essential files)
- ✅ Python environment
- ✅ Git repository status

### Agent Monitoring
- ✅ 26+ AI agents
- ✅ Agent documentation
- ✅ Bot infrastructure files

### Security Checks
- ✅ .env file protection
- ✅ .gitignore configuration
- ✅ Sensitive file detection
- ✅ Secret management

### Resource Thresholds
- Repository size warning: > 50 GB
- Logs directory warning: > 1 GB
- Cache directory warning: > 5 GB

## Integration

### GitHub Actions Workflow

The audit bot can be triggered via GitHub Actions:

```yaml
name: Daily System Audit

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

jobs:
  system-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Run System Audit
        run: |
          python scripts/system-audit.py --format all
      
      - name: Upload Audit Reports
        uses: actions/upload-artifact@v4
        with:
          name: audit-reports
          path: logs/system_audit_*.{md,json,txt}
      
      - name: Commit Reports
        run: |
          git config user.name "Audit Bot"
          git add logs/
          git commit -m "📋 Daily system audit completed"
          git push
```

### Monitoring Dashboard

Audit results can be integrated into the web dashboard:

```bash
# Generate audit and update dashboard
python scripts/system-audit.py --format json
python scripts/update-dashboard.py --audit-data logs/system_audit_latest.json
```

## Scheduled Operations

### Daily Audits
- **Time:** 6:00 AM UTC
- **Type:** Full system audit
- **Output:** All formats (MD, JSON, TXT)
- **Action:** Commit to repository

### Weekly Deep Audits
- **Time:** Sunday 6:00 AM UTC
- **Type:** Extended audit with performance metrics
- **Output:** Comprehensive report
- **Action:** Create GitHub Issue with summary

### On-Demand Audits
- Manual trigger via GitHub Actions
- Command line execution
- API invocation

## Alerts and Notifications

### Critical Alerts
- Security vulnerabilities detected
- Missing critical files
- Agent failures
- Data corruption

### Warning Alerts
- Resource threshold exceeded
- Missing documentation
- Configuration issues
- Optimization opportunities

## Best Practices

1. **Run audits regularly** - Daily automated audits catch issues early
2. **Review reports** - Human verification of automated findings
3. **Address issues promptly** - Fix degraded status items immediately
4. **Track trends** - Monitor audit history for patterns
5. **Update thresholds** - Adjust warning levels as system grows

## Audit History

All audit reports are stored in `logs/` directory:
- `system_audit_YYYYMMDD_HHMMSS.md` - Markdown report
- `system_audit_YYYYMMDD_HHMMSS.json` - JSON data
- `system_audit_YYYYMMDD_HHMMSS.txt` - Plain text report

## Troubleshooting

### Common Issues

**Issue: Permission denied when saving reports**
```bash
# Fix permissions
chmod -R u+w logs/
```

**Issue: Module not found errors**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Issue: Audit takes too long**
```bash
# Run in quiet mode
python scripts/system-audit.py --quiet
```

## Dependencies

- Python 3.8+
- Standard library only (no external dependencies)
- Git (for repository checks)

## Development

### Adding New Audit Sections

1. Add method to `SystemAuditor` class:
```python
def _audit_new_section(self):
    section = {
        "status": "OPERATIONAL",
        "checks": {},
        "issues": [],
        "recommendations": []
    }
    # Add checks here
    self.audit_results["sections"]["new_section"] = section
```

2. Call method in `run_full_audit()`:
```python
self._audit_new_section()
```

3. Update documentation

### Testing

```bash
# Test audit execution
python scripts/system-audit.py --format all

# Verify all reports generated
ls -la logs/system_audit_*

# Check JSON validity
python -m json.tool logs/system_audit_latest.json
```

## Related Documentation

- [AGENT_INFRASTRUCTURE.md](../AGENT_INFRASTRUCTURE.md) - Agent system overview
- [Bot-Usage-Guide.md](../../docs/Bot-Usage-Guide.md) - General bot documentation
- [System Monitoring](../../.github/workflows/agent-monitoring.yml) - Monitoring workflow

## Compliance

This audit bot follows:
- Security best practices
- Privacy protection standards
- Data integrity requirements
- Documentation standards

## Report Retention

- **Daily reports:** Retained for 90 days
- **Weekly reports:** Retained for 1 year
- **Critical incidents:** Retained indefinitely

## Support

For issues or questions:
- Open GitHub Issue with label `audit-bot`
- Review audit logs in `logs/` directory
- Check [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md)

---

**Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** System Audit Bot
**Status:** ✅ Production Ready
