# AutoAgentTestRepo

This is a test repository for string manipulation utilities, timezone services, and a basic counter implementation.

## Features

This package provides string manipulation utilities, timezone services, and a counter class with a focus on type safety, comprehensive testing, and clean code practices.

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
from src.nelson_time import get_current_time
from src.counter import Counter

# Reverse a string
result = reverse_string("hello")
print(result)  # Output: "olleh"

# Capitalize a string
result = capitalize_string("hello world")
print(result)  # Output: "Hello world"

# Get current time in Nelson, New Zealand
nelson_time = get_current_time()
print(nelson_time)  # Output: Current date and time in Nelson

# Use the counter
counter = Counter()
print(counter.get_value())  # Output: 1
counter.increment()
print(counter.get_value())  # Output: 2
```

## Counter

A basic counter implementation that starts at 1 and has a maximum value constraint of 10.

**Usage:**

```python
from src.counter import Counter

# Initialize counter (starts at 1)
counter = Counter()
print(counter.get_value())  # Output: 1

# Increment the counter
counter.increment()
print(counter.get_value())  # Output: 2

# Increment multiple times
for _ in range(5):
    counter.increment()
print(counter.get_value())  # Output: 7

# Counter can reach maximum value of 10
counter = Counter()
for _ in range(9):
    counter.increment()
print(counter.get_value())  # Output: 10
```

**Features:**
- Starts at value 1 by default
- Maximum value constraint of 10
- Simple increment operation
- Type-safe with full type hints
- 100% test coverage
- Clear and simple API

**API:**
- `__init__()` - Initialize counter at value 1
- `increment()` - Increment counter by 1
- `get_value() -> int` - Get current counter value
- `MAX_VALUE` - Class constant for maximum value (10)

For detailed documentation, see [Counter Design Documentation](docs/counter_design.md)

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

## Nelson Time Service

Get the current date and time in Nelson, New Zealand using the WorldTimeAPI service.

**Usage:**

```python
from src.nelson_time import get_current_time

# Get current time in Nelson
try:
    current_time = get_current_time()
    print(f"Current time in Nelson: {current_time}")
except Exception as e:
    print(f"Error fetching time: {e}")
```

**Features:**
- Fetches real-time data from WorldTimeAPI
- Uses Pacific/Auckland timezone (Nelson's timezone)
- Comprehensive error handling for network failures
- 5-second timeout for API requests
- Type-safe with full type hints
- Well-documented with detailed docstrings

**Error Handling:**

```python
from src.nelson_time import get_current_time, NelsonTimeError

try:
    time = get_current_time()
    print(time)
except NelsonTimeError as e:
    print(f"Failed to get Nelson time: {e}")
```

**API Integration:**

This service integrates with the free WorldTimeAPI service:
- Endpoint: `https://worldtimeapi.org/api/timezone/Pacific/Auckland`
- No authentication required
- Returns JSON with timezone and datetime information
- See [API Integration Documentation](docs/api_integration.md) for details

For detailed API documentation, see:
- [Counter Design Documentation](docs/counter_design.md)
- [String Utils Documentation](docs/string_utils.md)
- [API Integration Documentation](docs/api_integration.md)

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src

# Generate HTML coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_string_utils.py -v
pytest tests/test_nelson_time.py -v
pytest tests/test_counter.py -v
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
│   ├── nelson_time.py
│   └── counter.py
├── tests/
│   ├── __init__.py
│   ├── test_string_utils.py
│   ├── test_nelson_time.py
│   └── test_counter.py
├── docs/
│   ├── api_reference.md
│   ├── string_utils.md
│   ├── api_integration.md
│   └── counter_design.md
├── .gitignore
├── .mypy.ini
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Requirements

### Runtime Dependencies
- `requests` - HTTP library for API calls

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-cov` - Code coverage reporting
- `black>=23.0.0` - Code formatting
- `ruff>=0.1.0` - Fast Python linter
- `mypy>=1.5.0` - Static type checker

See `requirements-dev.txt` for specific versions.

## Documentation

For detailed documentation, see:
- [API Reference](docs/api_reference.md)
- [Counter Design Documentation](docs/counter_design.md)
- [String Utils Documentation](docs/string_utils.md)
- [API Integration Documentation](docs/api_integration.md)

## Contributing

1. Ensure all tests pass: `pytest tests/ -v`
2. Format code: `black src/ tests/`
3. Lint code: `ruff check src/ tests/`
4. Type check: `mypy src/`
5. Maintain test coverage above 90%

## License

MIT License