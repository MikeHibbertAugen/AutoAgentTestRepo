# AutoAgentTestRepo

This is a test repository for string manipulation utilities and timezone features.

## Features

This package provides string manipulation utilities and New Zealand datetime retrieval with a focus on type safety, comprehensive testing, and clean code practices.

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
from src.string_utils import reverse_string, capitalize_string
from src.nz_datetime import get_nz_datetime

# Reverse a string
result = reverse_string("hello")
print(result)  # Output: "olleh"

# Capitalize a string
result = capitalize_string("hello world")
print(result)  # Output: "Hello world"

# Get current New Zealand datetime
nz_time = get_nz_datetime()
print(nz_time)  # Output: {'datetime': '2024-01-15T14:30:45+13:00', 'timezone': 'Pacific/Auckland', ...}
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

### Capitalize String

Capitalize the first character of a string, leaving the rest unchanged.

**Usage:**

```python
from src.string_utils import capitalize_string

# Basic usage
result = capitalize_string("hello")
print(result)  # Output: "Hello"

# Works with sentences
result = capitalize_string("hello world")
print(result)  # Output: "Hello world"

# Already capitalized strings remain unchanged
result = capitalize_string("Hello")
print(result)  # Output: "Hello"

# Empty strings are handled safely
result = capitalize_string("")
print(result)  # Output: ""

# Handles mixed case
result = capitalize_string("hELLO")
print(result)  # Output: "HELLO"
```

**Features:**
- Type-safe with comprehensive input validation
- Handles empty strings and edge cases
- Preserves all characters except the first
- Idempotent operation
- 100% test coverage

For detailed API documentation, see [String Utils Documentation](docs/string_utils.md).

## New Zealand Datetime

Retrieve the current date and time in New Zealand timezone using the WorldTimeAPI.

**Usage:**

```python
from src.nz_datetime import get_nz_datetime

# Get current NZ datetime
result = get_nz_datetime()
print(result)
# Output: {
#     'datetime': '2024-01-15T14:30:45.123456+13:00',
#     'timezone': 'Pacific/Auckland',
#     'utc_offset': '+13:00',
#     'day_of_week': 1,
#     'day_of_year': 15
# }

# Handle errors gracefully
result = get_nz_datetime()
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Current NZ time: {result['datetime']}")
```

**Features:**
- Retrieves real-time datetime from WorldTimeAPI
- Returns structured data with timezone information
- Comprehensive error handling for network issues
- No authentication or API keys required
- Configurable timeout for API requests
- Full test coverage with mocked API calls

For detailed documentation, see [NZ Datetime Documentation](docs/nz_datetime.md).

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src

# Generate HTML coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_string_utils.py -v
pytest tests/test_nz_datetime.py -v
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
│   ├── string_utils.py
│   └── nz_datetime.py
├── tests/
│   ├── __init__.py
│   ├── test_string_utils.py
│   └── test_nz_datetime.py
├── docs/
│   ├── api_reference.md
│   ├── string_utils.md
│   └── nz_datetime.md
├── .gitignore
├── .mypy.ini
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Documentation

For detailed API documentation, see:
- [API Reference](docs/api_reference.md)
- [String Utils Documentation](docs/string_utils.md)
- [NZ Datetime Documentation](docs/nz_datetime.md)

## Contributing

1. Ensure all tests pass: `pytest tests/ -v`
2. Format code: `black src/ tests/`
3. Lint code: `ruff check src/ tests/`
4. Type check: `mypy src/`
5. Maintain test coverage above 90%

## License

MIT License