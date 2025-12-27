# Bot Development Guidelines

This guide provides guidelines for developing new bots and contributing to existing ones.

## Bot Architecture

### Standard Bot Structure

```
bot-name/
├── README.md           # Bot documentation
├── bot.py              # Main bot class
├── config.yml          # Bot configuration
├── requirements.txt    # Python dependencies
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_bot.py
│   └── fixtures/       # Test data
└── utils/              # Helper functions
    ├── __init__.py
    └── helpers.py
```

---

## Creating a New Bot

### Step 1: Plan Your Bot

Define:
- **Purpose:** What problem does it solve?
- **Input:** What data does it receive?
- **Output:** What does it produce?
- **Capacity:** How many operations per day?
- **Dependencies:** What services does it need?

### Step 2: Create Bot Directory

```bash
# Create bot directory
mkdir -p bots/my-new-bot/tests/fixtures
cd bots/my-new-bot

# Create basic files
touch README.md bot.py config.yml requirements.txt
touch tests/__init__.py tests/test_bot.py
```

### Step 3: Implement Bot Class

```python
# bot.py
"""
My New Bot - Brief description

This bot does X, Y, and Z.
"""

from typing import Dict, Any, Optional
import logging

class MyNewBot:
    """
    Main bot class for My New Bot.
    
    Attributes:
        config: Bot configuration dictionary
        logger: Python logger instance
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the bot.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self._setup()
    
    def _setup(self):
        """Initialize bot resources and connections."""
        self.logger.info("Setting up bot...")
        # Initialize Azure services, databases, etc.
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Main processing function.
        
        Args:
            input_data: Input to process
            
        Returns:
            Dictionary with processing results
            
        Raises:
            ValueError: If input is invalid
            RuntimeError: If processing fails
        """
        try:
            # Validate input
            self._validate_input(input_data)
            
            # Process
            result = self._do_processing(input_data)
            
            # Log result
            self.logger.info(f"Processed: {result}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing: {e}")
            raise
    
    def _validate_input(self, input_data: Any) -> None:
        """Validate input data."""
        if not input_data:
            raise ValueError("Input cannot be empty")
    
    def _do_processing(self, input_data: Any) -> Dict[str, Any]:
        """
        Perform the actual processing.
        
        Override this method in subclasses.
        """
        return {"status": "success", "data": input_data}


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="My New Bot")
    parser.add_argument("--file", help="Input file path")
    parser.add_argument("--config", help="Config file path")
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        import yaml
        with open(args.config) as f:
            config = yaml.safe_load(f)
    
    # Create and run bot
    bot = MyNewBot(config)
    result = bot.process(args.file)
    print(result)
```

### Step 4: Create Configuration

```yaml
# config.yml
bot_name: my-new-bot
version: 1.0.0

# Capacity limits
capacity:
  max_operations_per_day: 5000
  max_concurrent: 4
  timeout_seconds: 30

# Processing settings
processing:
  retry_attempts: 3
  retry_delay_seconds: 5
  batch_size: 10

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Dependencies
azure:
  cognitive_services:
    enabled: true
    endpoint: ${AZURE_COGNITIVE_ENDPOINT}
    key: ${AZURE_COGNITIVE_KEY}
```

### Step 5: Write Tests

```python
# tests/test_bot.py
"""
Unit tests for My New Bot
"""

import pytest
from bots.my_new_bot.bot import MyNewBot

class TestMyNewBot:
    """Test suite for MyNewBot class."""
    
    @pytest.fixture
    def bot(self):
        """Create a bot instance for testing."""
        return MyNewBot(config={"test_mode": True})
    
    def test_initialization(self, bot):
        """Test bot initializes correctly."""
        assert bot is not None
        assert bot.config["test_mode"] is True
    
    def test_process_valid_input(self, bot):
        """Test processing with valid input."""
        result = bot.process("test input")
        assert result["status"] == "success"
    
    def test_process_invalid_input(self, bot):
        """Test processing with invalid input."""
        with pytest.raises(ValueError):
            bot.process(None)
    
    def test_validate_input(self, bot):
        """Test input validation."""
        # Valid input should not raise
        bot._validate_input("valid")
        
        # Invalid input should raise
        with pytest.raises(ValueError):
            bot._validate_input(None)

# Integration tests
class TestMyNewBotIntegration:
    """Integration tests for MyNewBot."""
    
    def test_end_to_end_processing(self):
        """Test complete workflow."""
        bot = MyNewBot()
        result = bot.process("test data")
        
        assert "status" in result
        assert "data" in result
```

### Step 6: Document Your Bot

```markdown
# My New Bot

## Purpose
Brief description of what this bot does.

## Features
- Feature 1
- Feature 2
- Feature 3

## Configuration
...

## Usage
...

## Status
⚠️ In Development / ✅ Production Ready
```

---

## Code Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all classes and methods
- Keep functions small and focused
- Use meaningful variable names

### Code Quality Tools

```bash
# Install quality tools
pip install black pylint mypy pytest pytest-cov

# Format code
black bots/my-new-bot/

# Lint code
pylint bots/my-new-bot/

# Type check
mypy bots/my-new-bot/

# Run tests with coverage
pytest bots/my-new-bot/tests/ --cov --cov-report=html
```

---

## Testing Requirements

### Test Coverage
- Aim for 80%+ code coverage
- Test all public methods
- Test error conditions
- Test edge cases

### Test Types
1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test bot workflows
3. **End-to-End Tests** - Test with real data (limited)

### Running Tests

```bash
# Run all tests
pytest bots/ -v

# Run specific bot tests
pytest bots/my-new-bot/tests/ -v

# Run with coverage
pytest bots/my-new-bot/tests/ --cov=bots.my_new_bot --cov-report=html

# Run specific test
pytest bots/my-new-bot/tests/test_bot.py::TestMyNewBot::test_process_valid_input -v
```

---

## Integration with Repository

### Add to Bot Infrastructure

1. Update `bots/README.md` to include your bot
2. Update `bots/AGENT_INFRASTRUCTURE.md` with capacity info
3. Add to bot orchestration workflow

### Create GitHub Actions Workflow

```yaml
# .github/workflows/my-new-bot.yml
name: My New Bot

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r bots/my-new-bot/requirements.txt
      
      - name: Run bot
        env:
          AZURE_COGNITIVE_KEY: ${{ secrets.AZURE_COGNITIVE_KEY }}
        run: |
          python bots/my-new-bot/bot.py --config bots/my-new-bot/config.yml
```

---

## Best Practices

### Error Handling
- Always use try-except blocks
- Log errors with context
- Raise appropriate exception types
- Provide helpful error messages

### Logging
- Use Python's logging module
- Log important events
- Include context in log messages
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)

### Configuration
- Use environment variables for secrets
- Use config files for settings
- Validate configuration on startup
- Provide sensible defaults

### Performance
- Use batch processing when possible
- Implement caching for repeated operations
- Set appropriate timeouts
- Monitor resource usage

### Security
- Never commit secrets or API keys
- Validate all input
- Use secure connections (HTTPS)
- Follow principle of least privilege

---

## Contributing

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-new-bot`
2. Implement bot following this guide
3. Write tests (80%+ coverage)
4. Update documentation
5. Run quality checks: `black`, `pylint`, `mypy`, `pytest`
6. Commit with clear messages
7. Push and create pull request
8. Address review feedback

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests pass and coverage is adequate
- [ ] Documentation is complete
- [ ] No secrets in code
- [ ] Error handling is robust
- [ ] Logging is appropriate
- [ ] Configuration is externalized

---

## Resources

### Documentation
- [Python Documentation](https://docs.python.org/3/)
- [Azure SDK for Python](https://docs.microsoft.com/en-us/azure/developer/python/)
- [pytest Documentation](https://docs.pytest.org/)

### Examples
- [pdf-analysis-bot](pdf-analysis-bot/) - Full example
- [search-bot](search-bot/) - Search implementation

### Support
- GitHub Issues for bugs
- GitHub Discussions for questions
- [Contributing Guidelines](../CONTRIBUTING.md)

---

*Last Updated: December 2024*
