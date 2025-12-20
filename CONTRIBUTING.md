# Contributing to the Epstein Files Codex

Thank you for your interest in contributing to this important public resource. This guide will help you understand how to contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [What Can I Contribute?](#what-can-i-contribute)
- [Document Submission](#document-submission)
- [Verification Process](#verification-process)
- [Technical Contributions](#technical-contributions)
- [Style Guidelines](#style-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Standards

- **Factual Accuracy**: All contributions must be based on verified public records
- **Respect for Victims**: Maintain dignity and privacy for all victims
- **No Speculation**: Stick to documented facts from credible sources
- **Professional Conduct**: Maintain respectful, professional communication
- **Legal Compliance**: Follow all applicable laws regarding sealed documents and privacy

### Unacceptable Behavior

- Posting unverified claims or speculation
- Doxxing or exposing personal information not in public record
- Harassing or disrespectful communication
- Submitting copyrighted material without permission
- Attempting to access or share sealed court documents

## What Can I Contribute?

### 1. Documents

- Court filings from public records (PACER, court websites)
- Government documents obtained through FOIA
- Published investigative journalism from credible sources
- Flight logs and travel records from public sources
- Property records from county/state databases
- Financial documents from public filings

### 2. Metadata & Organization

- Improving document categorization
- Adding tags and keywords
- Correcting dates or attribution
- Enhancing cross-references
- Improving character directory entries

### 3. Technical Improvements

- Bug fixes
- Performance improvements
- New features for organization or presentation
- Improving search functionality
- Enhancing AI agent capabilities

### 4. Documentation

- Improving README and guides
- Adding usage examples
- Clarifying processes
- Creating tutorials

## Document Submission

### Submission Methods

#### Method 1: Web Upload (Recommended for Most Users)

1. Visit [Upload Page](https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/upload.html)
2. Select your PDF file(s)
3. Wait for automated analysis
4. Documents scoring 70+ automatically indexed

#### Method 2: GitHub Issue

1. Create a new issue with label `document-submission`
2. Provide:
   - Link to document source
   - Brief description
   - Date/context
   - Why it's relevant
3. AI agents will retrieve and process

#### Method 3: Pull Request

1. Fork the repository
2. Add document to `data/uploads/` directory
3. Include metadata file: `document_name.json`
4. Create pull request
5. Automated workflow will analyze and route

### Metadata Format

```json
{
  "title": "Document Title",
  "date": "2024-01-01",
  "source": "SDNY Court",
  "case_number": "19-cr-490",
  "category": "legal",
  "description": "Brief description",
  "verification_level": 1,
  "url": "https://source-url.com"
}
```

## Verification Process

All submitted documents go through verification:

### Automated Verification (AI Agents)

1. **PDF Analysis**: Content analysis for relevance
2. **Source Check**: Verify document origin
3. **Duplicate Detection**: Check for existing copies
4. **OCR Processing**: Extract text from scanned documents
5. **Entity Extraction**: Identify people, places, organizations
6. **Cross-Reference**: Link to related documents

### Manual Review (When Needed)

Documents scoring 40-69% relevance or flagged for other reasons enter manual review queue.

### Verification Levels

- **Level 1**: Official court documents (PACER verified)
- **Level 2**: Government records (FOIA verified)
- **Level 3**: Verified media from credible sources
- **Level 4**: Secondary sources
- **Level 5**: Pending verification

## Technical Contributions

### Development Setup

```bash
# Clone repository
git clone https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# Install dependencies (if adding new bots)
pip install -r bots/requirements.txt

# Run tests
pytest tests/
```

### Bot Development

When creating new AI agents:

1. Follow existing bot structure in `bots/` directory
2. Include README with capabilities and configuration
3. Add to agent infrastructure documentation
4. Create corresponding GitHub Actions workflow
5. Include error handling and logging
6. Write unit tests

### Web Development

For website changes:

1. Maintain responsive design
2. Follow existing CSS patterns in `web/css/styles.css`
3. Ensure accessibility (WCAG 2.1 AA)
4. Test across browsers
5. Maintain dark theme consistency

## Style Guidelines

### Documentation

- Use Markdown for all documentation
- Include table of contents for long documents
- Use clear, descriptive headings
- Provide examples where helpful
- Keep line length under 100 characters

### Code

#### Python (Bot Development)

```python
# Follow PEP 8
# Use type hints
# Include docstrings

def analyze_document(file_path: str, threshold: int = 70) -> AnalysisResult:
    """
    Analyze PDF for Epstein-related content.
    
    Args:
        file_path: Path to PDF file
        threshold: Minimum relevance score (0-100)
    
    Returns:
        AnalysisResult object with scores and routing decision
    """
    pass
```

#### JavaScript

```javascript
// Use ES6+ features
// Descriptive variable names
// Comments for complex logic

function performSearch(query) {
    if (!query || query.trim() === '') {
        alert('Please enter a search query');
        return;
    }
    
    // Call search API
    searchDocuments(query);
}
```

### HTML/CSS

- Semantic HTML5
- BEM naming convention for CSS
- Mobile-first responsive design
- Accessibility attributes (aria-labels, alt text)

## Pull Request Process

### Before Submitting

1. **Test Your Changes**: Ensure all tests pass
2. **Update Documentation**: Keep docs in sync with changes
3. **Follow Style Guide**: Match existing code style
4. **Check Lint**: Run linters before committing
5. **Small, Focused PRs**: One logical change per PR

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Document submission
- [ ] Performance improvement

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Follows style guide
- [ ] No breaking changes
- [ ] Commits are descriptive
```

### Review Process

1. **Automated Checks**: CI workflows must pass
2. **Code Review**: At least one maintainer approval
3. **Document Verification**: For document submissions
4. **Testing**: Verify functionality works as expected
5. **Merge**: Squash and merge after approval

### After Merge

- PR closes automatically
- Changes deployed to GitHub Pages (web changes)
- AI agents process new documents (document submissions)
- Documentation builds updated

## Reporting Issues

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Browser/system info

### Feature Requests

Include:
- Clear description of feature
- Use case and motivation
- Example of how it would work
- Any relevant research

## Communication

### Channels

- **GitHub Issues**: Bug reports, features, questions
- **Pull Requests**: Code contributions, document submissions
- **Discussions**: General discussion, ideas, Q&A

### Response Times

- Bug reports: 48 hours
- Feature requests: 1 week
- PRs: 3-5 days
- Document submissions: Automated (immediate), manual review (1 week)

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Website credits page

## Legal

### License

By contributing, you agree that your contributions will be licensed under the project's license.

### Rights

- You must have rights to submit any documents
- No copyrighted material without permission
- Respect all applicable laws
- Follow ethical guidelines

### Disclaimer

This project deals with serious criminal matters. All contributors must:
- Maintain professionalism
- Respect legal boundaries
- Protect victim privacy
- Verify all information

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues for similar questions
3. Open a new issue with the `question` label
4. Be specific and provide context

---

**Thank you for contributing to this important public resource.**

*Last Updated: December 2024*
