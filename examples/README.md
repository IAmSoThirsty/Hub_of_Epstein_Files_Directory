# Epstein Files Hub - Examples

This directory contains example scripts demonstrating how to use the Epstein Files Hub library.

## Examples

### 1. basic_usage.py
Basic usage of the Hub library:
- Initialize Hub
- Fetch public files
- Process documents
- Generate search index
- Get statistics
- Cleanup

```bash
python examples/basic_usage.py
```

### 2. advanced_usage.py
Advanced usage with subsystem access:
- Custom configuration
- Full pipeline execution
- Direct subsystem access
- Cache management
- Detailed statistics

```bash
python examples/advanced_usage.py
```

### 3. context_manager.py
Using Hub as a context manager:
- Automatic resource management
- Cleanup on exit
- Exception safety

```bash
python examples/context_manager.py
```

## Running Examples

### Prerequisites
```bash
# Install the library
pip install -e .

# Or install requirements
pip install -r requirements.txt
```

### Execute
```bash
# Run basic example
python examples/basic_usage.py

# Run advanced example
python examples/advanced_usage.py

# Run context manager example
python examples/context_manager.py
```

## Expected Output

Each example will display:
1. Initialization status
2. Operation progress
3. Results and statistics
4. Cleanup information

## Support

For more information:
- See docs/LIBRARY_DOCUMENTATION.md
- Check README.md
- Visit GitHub Issues
