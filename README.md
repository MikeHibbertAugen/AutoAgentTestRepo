# AutoAgentTestRepo

This is a test repository for string manipulation utilities, timezone services, a configurable counter implementation, a text-based adventure game world location system, and mathematical utilities including Pi calculation.

## Features

This package provides string manipulation utilities, timezone services, a counter class, a location-based game world system, and mathematical utilities with a focus on type safety, comprehensive testing, and clean code practices.

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
from src.location import Location
from src.math_utils import calculate_pi

# Reverse a string
result = reverse_string("hello")
print(result)  # Output: "olleh"

# Capitalize a string
result = capitalize_string("hello world")
print(result)  # Output: "Hello world"

# Get current time in Nelson, New Zealand
nelson_time = get_current_time()
print(nelson_time)  # Output: Current date and time in Nelson

# Use the counter with default range (1 to 10)
counter = Counter()
print(counter.current)  # Output: 1
counter.increment()
print(counter.current)  # Output: 2

# Use the counter with custom range
counter = Counter(start=5, end=15)
print(counter.current)  # Output: 5
counter.increment()
print(counter.current)  # Output: 6

# Create game locations
beach = Location("Muriwai Beach", "A beautiful black sand beach on the west coast")
forest = Location("Waitakere Ranges", "Dense native forest with walking trails")

# Connect locations
beach.add_exit("east", forest)
forest.add_exit("west", beach)

# Navigate between locations
print(beach.name)  # Output: Muriwai Beach
print(beach.get_available_exits())  # Output: ['east']
next_location = beach.get_exit("east")
print(next_location.name)  # Output: Waitakere Ranges

# Calculate Pi to 6 decimal places
pi_value = calculate_pi()
print(f"Pi = {pi_value:.6f}")  # Output: Pi = 3.141593
```

## Mathematical Utilities

### Pi Calculation

Calculate the value of Pi (π) to 6 decimal places using an efficient mathematical algorithm.

**Usage:**

```python
from src.math_utils import calculate_pi

# Calculate Pi
pi_value = calculate_pi()
print(pi_value)  # Output: 3.141592653589793

# Format to 6 decimal places
print(f"Pi = {pi_value:.6f}")  # Output: Pi = 3.141593
```

**Features:**
- Accurate to 6 decimal places (3.141593)
- Uses Machin's formula for fast convergence
- Pure mathematical computation with no external dependencies
- Deterministic output (same result every time)
- Type-safe with full type hints
- 100% test coverage

**Algorithm:**
The implementation uses Machin's formula, which provides excellent convergence for calculating Pi. This formula is significantly faster than simpler methods like the Leibniz formula.

For detailed documentation about the algorithm and performance characteristics, see [Pi Calculation Documentation](docs/pi_calculation.md)

## Game World Location System

A text-based adventure game location system set in north-west Auckland, featuring interconnected locations that players can navigate through.

**Usage:**

```python
from src.location import Location

# Create locations
beach = Location("Muriwai Beach", "A beautiful black sand beach on the west coast")
forest = Location("Waitakere Ranges", "Dense native forest with walking trails")
cafe = Location("Piha Cafe")  # Description is optional

# Connect locations with directional exits
beach.add_exit("east", forest)
beach.add_exit("north", cafe)
forest.add_exit("west", beach)
cafe.add_exit("south", beach)

# Query location information
print(beach.name)  # Output: Muriwai Beach
print(beach.description)  # Output: A beautiful black sand beach on the west coast
print(beach.get_available_exits())  # Output: ['east', 'north']

# Navigate between locations
next_location = beach.get_exit("east")
if next_location:
    print(f"You travel east to {next_location.name}")
    # Output: You travel east to Waitakere Ranges

# Check for invalid exits
unknown = beach.get_exit("west")
print(unknown)  # Output: None
```

**Features:**
- Location creation with name and optional description
- Directional exits connecting locations (north, south, east, west, etc.)
- Query available exits from any location
- Navigate between connected locations
- Type-safe with full type hints
- Comprehensive error handling
- 100% test coverage
- BDD scenarios for behavior validation

**API:**
- `__init__(name: str, description: str = "")` - Create a location with name and optional description
- `add_exit(direction: str, destination: Location) -> None` - Add an exit in a specific direction
- `get_exit(direction: str) -> Optional[Location]` - Get the destination location for a direction
- `get_available_exits() -> List[str]` - Get list of all available exit directions
- `name: str` - Property to access location name
- `description: str` - Property to access location description

**Example Game World:**

```python
from src.location import Location

# Create a connected world in north-west Auckland
muriwai = Location("Muriwai Beach", "Black sand beach with dramatic gannet colony")
piha = Location("Piha Beach", "Famous surf beach with Lion Rock")
karekare = Location("Karekare Beach", "Secluded beach surrounded by cliffs")
ranges = Location("Waitakere Ranges", "Ancient rainforest with native birds")
arataki = Location("Arataki Visitor Centre", "Information center with panoramic views")

# Connect the locations
muriwai.add_exit("south", ranges)
ranges.add_exit("north", muriwai)
ranges.add_exit("west", piha)
ranges.add_exit("south", arataki)
piha.add_exit("east", ranges)
piha.add_exit("south", karekare)
karekare.add_exit("north", piha)
arataki.add_exit("north", ranges)

# Explore the world
current = muriwai
print(f"You are at: {current.name}")
print(f"Description: {current.description}")
print(f"Available exits: {', '.join(current.get_available_exits())}")
```

For detailed documentation, see [Location Architecture Documentation](docs/architecture.md)

## Counter

A configurable counter implementation with customizable start and end values, supporting initialization, increment, reset, boundary checking, and display/output functionality.

**Usage:**

```python
from src.counter import Counter

# Initialize counter with default range (1 to 10)
counter = Counter()
print(counter.current)  # Output: 1

# Increment the counter
counter.increment()
print(counter.current)  # Output: 2

# Check if counter has reached end value
print(counter.has_reached_end())  # Output: False

# Increment multiple times
for _ in range(8):
    counter.increment()
print(counter.current)  # Output: 10
print(counter.has_reached_end())  # Output: True

# Try to increment beyond end value
try:
    counter.increment()
except ValueError as e:
    print(e)  # Output: Cannot increment beyond end value

# Reset the counter
counter.reset()
print(counter.current)  # Output: 1

# Initialize with custom range
counter = Counter(start=5, end=15)
print(counter.current)  # Output: 5
counter.increment()
print(counter.current)  # Output: 6

# Negative ranges are supported
counter = Counter(start=-5, end=5)
print(counter.current)  # Output: -5
```

**Display and Output Features:**

```python
from src.counter import Counter

# Get all counter values as a list
counter = Counter(start=1, end=10)
all_values = counter.get_all_values()
print(all_values)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Display current value
counter.display_current()  # Prints: 1

# Print all values sequentially
counter.print_all()
# Output:
# 1
# 2
# 3
# ...
# 10

# Get values as formatted string
formatted = counter.to_string()
print(formatted)  # Output: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
```

**CLI Usage:**

The counter can also be run as a command-line tool with customizable start and end parameters.

Run the counter with default parameters (1 to 10):
```bash
python src/counter_cli.py
```

Customize the starting number:
```bash
python src/counter_cli.py --start 5
```

Customize the ending number:
```bash
python src/counter_cli.py --end 15
```

Customize both parameters:
```bash
python src/counter_cli.py --start 3 --end 7
```

Display help information:
```bash
python src/counter_cli.py --help
```

**CLI Features:**
- Configurable start and end values via command-line arguments
- Default range from 1 to 10
- Comprehensive error handling for invalid inputs
- Clear help documentation
- User-friendly error messages
- Proper exit codes for CI/CD integration

**Features:**
- Configurable start and end values
- Default range from 1 to 10
- Increment with automatic boundary checking
- Reset functionality to return to start value
- Check if counter has reached end value
- Raises `ValueError` when attempting to increment beyond end
- **Display and output methods for flexible value retrieval**
- **Get all values as a list**
- **Print current or all values to stdout**
- **Format values as comma-separated strings**
- **Command-line interface for standalone execution**
- Type-safe with full type hints
- 100% test coverage
- Clear and simple API

**API:**
- `__init__(start: int = 1, end: int = 10)` - Initialize counter with optional start and end values
- `increment() -> None` - Increment counter by 1, raises `ValueError` if at end value
- `reset() -> None` - Reset counter to start value
- `has_reached_end() -> bool` - Check if counter is at end value
- `current: int` - Public attribute for current counter value
- `get_all_values() -> list[int]` - Return list of all counter values from start to end
- `get_current_value() -> int` - Return the current counter value
- `display_current() -> None` - Print the current value to stdout
- `print_all() -> None` - Print each counter value on a separate line
- `to_string() -> str` - Return counter values as a comma-separated string

For detailed documentation, see [Counter API Documentation](docs/counter_api.md) and [Counter Display Documentation](docs/counter_display.md)

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
- [Counter API Documentation](docs/counter_api.md)
- [Counter Display Documentation](docs/counter_display.md)
- [String Utils Documentation](docs/string_utils.md)
- [API Integration Documentation](docs/api_integration.md)
- [Location Architecture Documentation](docs/architecture.md)
- [Pi Calculation Documentation](docs/pi_calculation.md)

## Development

### Running Tests

```bash
# Run all unit tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_string_utils.py -v
pytest tests/test_nelson_time.py -v
pytest tests/test_counter.py -v
pytest tests/test_counter_cli.py -v
pytest tests/test_location.py -v
pytest tests/test_math_utils.py -v

# Run BDD tests with behave
behave tests/features/

# Run location-specific tests
pytest tests/test_location.py -v --cov=src/location
behave tests/features/location.feature

# Generate HTML coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run all tests (unit + BDD)
pytest tests/ -v --cov=src && behave tests/features/
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
│   ├── counter.py
│   ├── counter_cli.py
│   ├── location.py
│   └── math_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_string_utils.py
│   ├── test_nelson_time.py
│   ├── test_counter.py
│   ├── test_counter_cli.py
│   ├── test_location.py
│   ├── test_math_utils.py
│   └── features/
│       ├── __init__.py
│       ├── counter.feature
│       ├── location.feature
│       ├── environment.py
│       └── steps/
│           ├── __init__.py
│           ├── counter_steps.py
│           └── location_steps.py
├── docs/
│   ├── api_reference.md
│   ├── string_utils.md
│   ├── api_integration.md
│   ├── counter_api.md
│   ├── counter_display.md
│   ├── architecture.md
│   └── pi_calculation.md
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
- `pytest` - Testing framework
- `pytest-cov` - Code coverage reporting
- `behave` - BDD testing framework
- `black` - Code formatting
- `ruff` - Fast Python linter
- `mypy` - Static type checker

See `requirements-dev.txt` for specific versions.

## Documentation

For detailed API documentation, see:
- [API Reference](docs/api_reference.md)
- [Counter API Documentation](docs/counter_api.md)
- [Counter Display Documentation](docs/counter_display.md)
- [String Utils Documentation](docs/string_utils.md)
- [API Integration Documentation](docs/api_integration.md)
- [Location Architecture Documentation](docs/architecture.md)
- [Pi Calculation Documentation](docs/pi_calculation.md)

## Contributing

1. Ensure all tests pass: `pytest tests/ -v && behave tests/features/`
2. Format code: `black src/ tests/`
3. Lint code: `ruff check src/ tests/`
4. Type check: `mypy src/`
5. Maintain test coverage above 95%

## License

MIT License