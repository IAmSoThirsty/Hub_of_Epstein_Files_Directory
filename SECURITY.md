# Security Policy

## Overview

This document outlines the security policies and procedures for the Epstein Files Hub Directory project. We are committed to maintaining the highest standards of security, following CIA principles (Confidentiality, Integrity, Availability).

## Security Principles

### Confidentiality
- All data sources are from public records only
- No private or sensitive information is stored
- Victim privacy is protected per court orders
- Access controls prevent unauthorized access

### Integrity
- All files verified with SHA-256 checksums
- Data validation on all inputs
- Immutable audit logs
- Version control for all changes

### Availability
- 99.9%+ uptime through GitHub Pages
- Redundant backups
- Graceful degradation
- DDoS protection via Cloudflare

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

### Where to Report

**DO NOT** open public issues for security vulnerabilities.

Instead, please report security vulnerabilities to:
- **GitHub Security Advisory**: Use the "Security" tab in this repository
- **Email**: Contact maintainers via GitHub profile
- **Encrypted**: PGP key available on request

### What to Include

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 24 hours
- **Status Update**: Within 72 hours
- **Resolution**: Depends on severity
  - Critical: Within 7 days
  - High: Within 30 days
  - Medium: Within 90 days
  - Low: Next release cycle

## Security Measures

### Code Security

1. **Dependency Management**
   - All dependencies pinned to specific versions
   - Regular security audits with `pip audit`
   - Automated dependency updates with Dependabot
   - CVE monitoring for all packages

2. **Static Analysis**
   - CodeQL scanning on all commits
   - Bandit security linter
   - MyPy type checking
   - Flake8 code quality

3. **Secrets Management**
   - No secrets in code
   - `.env` files excluded from git
   - GitHub Secrets for CI/CD
   - Secret scanning enabled

### Infrastructure Security

1. **Web Security**
   - HTTPS enforced (GitHub Pages + Cloudflare)
   - Security headers (CSP, HSTS, X-Frame-Options)
   - DDoS protection (Cloudflare)
   - Rate limiting on APIs

2. **Container Security**
   - Non-root user in Docker containers
   - Multi-stage builds
   - Minimal base images
   - Regular image scanning

3. **Access Control**
   - GitHub CODEOWNERS for protected files
   - Branch protection rules
   - Required reviews for PRs
   - 2FA required for maintainers

### Data Security

1. **Input Validation**
   - All user inputs validated
   - File upload size limits
   - MIME type verification
   - Sanitization of file names

2. **Data Integrity**
   - SHA-256 checksums for all files
   - Digital signatures for releases
   - Audit logs for all changes
   - Version control for data

3. **Privacy Protection**
   - No PII collection
   - Cookie consent (if implemented)
   - GDPR compliance
   - Data minimization

## Security Best Practices for Contributors

### Code Contributions

1. **Never commit:**
   - API keys or tokens
   - Passwords or credentials
   - Private keys or certificates
   - Personal information

2. **Always:**
   - Use `.env` files for secrets
   - Validate all inputs
   - Use parameterized queries
   - Follow secure coding guidelines

3. **Dependencies:**
   - Only add necessary dependencies
   - Verify package authenticity
   - Check for known vulnerabilities
   - Use pinned versions

### Docker Best Practices

1. **Container Security:**
   - Use official base images
   - Run as non-root user
   - Minimize installed packages
   - Scan images for vulnerabilities

2. **Network Security:**
   - Limit exposed ports
   - Use internal networks
   - Enable TLS for communications
   - Implement network policies

### GitHub Actions Security

1. **Workflow Security:**
   - Pin actions to specific commits
   - Use minimal permissions
   - Store secrets in GitHub Secrets
   - Review third-party actions

2. **Artifact Security:**
   - Verify artifact integrity
   - Sign releases
   - Use checksums
   - Limit artifact retention

## Security Checklist

Before deploying, ensure:

- [ ] All dependencies updated and scanned
- [ ] No secrets in code
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Access controls in place
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Incident response plan documented
- [ ] Security scanning enabled
- [ ] Audit logging configured

## Compliance

This project maintains compliance with:

- **OWASP Top 10**: Protection against common vulnerabilities
- **CWE Top 25**: Mitigation of most dangerous software weaknesses
- **GDPR**: Privacy by design
- **GitHub Security Best Practices**: Following official guidelines

## Incident Response

### Detection
- Automated monitoring
- Security scanning
- User reports
- Third-party disclosures

### Response Process

1. **Contain**: Isolate affected systems
2. **Assess**: Determine impact and scope
3. **Remediate**: Apply fixes
4. **Communicate**: Notify affected parties
5. **Document**: Record incident details
6. **Learn**: Update procedures

### Communication

- Security advisories via GitHub
- Email notifications for critical issues
- Status page updates
- Post-mortem reports (if applicable)

## Security Contacts

- **Security Team**: Available via GitHub Security tab
- **Emergency**: Create security advisory
- **General Questions**: GitHub Discussions

## Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged in:
- SECURITY.md
- Release notes
- Hall of Fame (if implemented)

## Updates

This security policy is reviewed and updated:
- Quarterly
- After security incidents
- When new threats emerge
- When infrastructure changes

**Last Updated**: February 1, 2026  
**Version**: 1.0.0  
**Next Review**: May 1, 2026
