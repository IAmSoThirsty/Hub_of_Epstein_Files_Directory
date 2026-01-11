# Test Suite for Epstein Files Hub

This directory contains comprehensive tests for the Epstein Files Hub project.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Shared fixtures and configuration
├── unit/                # Unit tests for individual scripts
│   ├── test_fetch_public_files.py
│   ├── test_fetch_wikipedia_data.py
│   ├── test_generate_search_index.py
│   ├── test_process_pdfs.py
│   ├── test_safe_source_expander.py
│   ├── test_manage_volunteer_access.py
│   └── test_system_audit.py
├── integration/         # Integration tests for workflows
│   └── test_data_workflows.py
├── docker/              # Docker container tests
│   └── test_containers.py
└── e2e/                 # End-to-end workflow tests
    └── test_workflows.py
```

## Running Tests

### Run All Tests

```bash
# Using pytest directly
pytest

# Using make command
make test

# With coverage report
make test-cov
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Docker tests only
pytest -m docker

# End-to-end tests only
pytest -m e2e

# Exclude slow tests
pytest -m "not slow"

# Exclude network-dependent tests
pytest -m "not network"
```

### Run Tests for Specific Script

```bash
# Test search index generation
pytest tests/unit/test_generate_search_index.py

# Test PDF processing
pytest tests/unit/test_process_pdfs.py

# Test Wikipedia data fetching
pytest tests/unit/test_fetch_wikipedia_data.py
```

## Test Markers

Tests are marked with the following markers:

- `@pytest.mark.unit` - Unit tests for individual functions/classes
- `@pytest.mark.integration` - Integration tests for workflows
- `@pytest.mark.docker` - Docker container tests
- `@pytest.mark.e2e` - End-to-end workflow tests
- `@pytest.mark.slow` - Tests that take a long time to run
- `@pytest.mark.network` - Tests that require network access

## Test Coverage

To generate a coverage report:

```bash
# Generate coverage report
pytest --cov=scripts --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Coverage reports show:
- Line coverage for all scripts
- Branch coverage
- Missing lines
- Coverage percentage

## Writing New Tests

### Test File Naming

- Unit tests: `test_<script_name>.py`
- Integration tests: `test_<workflow_name>.py`
- Docker tests: `test_<component>.py`
- E2E tests: `test_<journey_name>.py`

### Test Function Naming

- Use descriptive names: `test_<what_is_being_tested>`
- Example: `test_pdf_file_detection`, `test_search_index_generation`

### Using Fixtures

Common fixtures are defined in `conftest.py`:

```python
def test_something(temp_dir, mock_data_dir):
    """Test uses temporary directory and mock data."""
    # temp_dir is a temporary directory
    # mock_data_dir has data/ structure
    pass
```

### Test Structure

```python
import pytest

@pytest.mark.unit
class TestFeature:
    """Test suite for specific feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        assert True
    
    @pytest.mark.parametrize("input,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
    ])
    def test_with_parameters(self, input, expected):
        """Test with multiple parameters."""
        assert input is not None
```

## Continuous Integration

Tests are automatically run in CI/CD:

- On every pull request
- On push to main branch
- Daily scheduled run

See `.github/workflows/test.yml` for CI configuration.

## Test Dependencies

Test dependencies are listed in `requirements-dev.txt`:

- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `pytest-mock` - Mocking plugin
- `pytest-asyncio` - Async test support

Install with:

```bash
pip install -r requirements-dev.txt
```

## Troubleshooting

### Tests Fail Locally

1. Ensure dependencies are installed: `pip install -r requirements-dev.txt`
2. Check Python version: `python --version` (requires 3.8+)
3. Clear pytest cache: `pytest --cache-clear`

### Import Errors

Make sure the project root is in PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Slow Tests

Skip slow tests during development:

```bash
pytest -m "not slow"
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Use descriptive test names
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **Mock External Services**: Don't make real network calls in unit tests
5. **Fast Tests**: Keep unit tests fast (<1s each)
6. **Coverage**: Aim for 80%+ coverage

## Contributing

When contributing:

1. Write tests for new features
2. Maintain existing test coverage
3. Run tests before committing: `make test`
4. Run linters: `make lint`
5. Check types: `make type-check`

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
