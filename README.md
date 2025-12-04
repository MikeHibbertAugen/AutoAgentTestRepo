# AutoAgentTestRepo

This is a test repository for string manipulation utilities.

## Features

This package provides string manipulation utilities with a focus on type safety, comprehensive testing, and clean code practices.

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AutoAgentTestRepo.git
cd AutoAgentTestRepo

# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### Quick Start

```python
from src.string_utils import reverse_string

# Reverse a string
result = reverse_string("hello")
print(result)  # Output: "olleh"
```

## String Operations

### Reverse String

Reverse any string efficiently and safely with full Unicode support.

**Usage:**

```python
from src.string_utils import reverse_string

# Basic usage
result = reverse_string("hello")
print(result)  # Output: "olleh"

# Works with spaces and special characters
result = reverse_string("Hello, World!")
print(result)  # Output: "!dlroW ,olleH"

# Handles Unicode characters
result = reverse_string("Hello 👋 World")
print(result)  # Output: "dlroW 👋 olleH"

# Empty strings are handled safely
result = reverse_string("")
print(result)  # Output: ""

# Single character strings
result = reverse_string("A")
print(result)  # Output: "A"
```

**Features:**
- Type-safe with comprehensive input validation
- Handles empty strings and single characters
- Full Unicode support (emojis, special characters, etc.)
- Efficient O(n) implementation
- Comprehensive error handling with clear error messages
- 100% test coverage

**Error Handling:**

```python
from src.string_utils import reverse_string

# TypeError is raised for non-string inputs
try:
    reverse_string(123)
except TypeError as e:
    print(e)  # Output: "Input must be a string, got <class 'int'>"
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src

# Generate HTML coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_string_utils.py -v
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint code with Ruff
ruff check src/ tests/

# Type check with MyPy
mypy src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest tests/ -v --cov=src
```

### Project Structure

```
AutoAgentTestRepo/
├── src/
│   ├── __init__.py
│   └── string_utils.py
├── tests/
│   ├── __init__.py
│   └── test_string_utils.py
├── docs/
│   └── api_reference.md
├── .gitignore
├── .mypy.ini
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Documentation

For detailed API documentation, see [API Reference](docs/api_reference.md).

## Contributing

1. Ensure all tests pass: `pytest tests/ -v`
2. Format code: `black src/ tests/`
3. Lint code: `ruff check src/ tests/`
4. Type check: `mypy src/`
5. Maintain test coverage above 90%

## License

MIT License