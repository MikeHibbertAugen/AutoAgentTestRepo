# Counter API Documentation

## Overview

The `Counter` class provides a simple, configurable counter with boundary checking capabilities. It supports initialization with custom start and end values, incrementation, reset functionality, and boundary state checking.

## Module

```python
from src.counter import Counter
```

## Class: Counter

### Constructor

#### `__init__(start: int = 1, end: int = 10)`

Initialize a new Counter instance with configurable start and end values.

**Parameters:**

- `start` (int, optional): The starting value of the counter. Defaults to 1.
- `end` (int, optional): The ending value of the counter (inclusive). Defaults to 10.

**Raises:**

- `ValueError`: If `start` is greater than `end`.

**Example:**

```python
# Default counter (1 to 10)
counter = Counter()

# Custom range counter
counter = Counter(start=0, end=100)

# Single value counter
counter = Counter(start=5, end=5)

# Negative range counter
counter = Counter(start=-10, end=-1)
```

### Attributes

#### `current: int`

The current value of the counter. Initially set to the `start` value.

**Type:** `int`

**Example:**

```python
counter = Counter(start=5, end=10)
print(counter.current)  # Output: 5
```

#### `start: int`

The starting value of the counter (read-only after initialization).

**Type:** `int`

#### `end: int`

The ending value of the counter (read-only after initialization).

**Type:** `int`

### Methods

#### `increment() -> None`

Increment the counter by 1.

**Returns:** `None`

**Raises:**

- `ValueError`: If the counter has already reached the end value. Use `has_reached_end()` to check before incrementing if needed.

**Example:**

```python
counter = Counter(start=1, end=3)
print(counter.current)  # Output: 1

counter.increment()
print(counter.current)  # Output: 2

counter.increment()
print(counter.current)  # Output: 3

# This will raise ValueError
try:
    counter.increment()
except ValueError as e:
    print(f"Error: {e}")  # Output: Error: Counter has reached its end value
```

#### `reset() -> None`

Reset the counter to its starting value.

**Returns:** `None`

**Example:**

```python
counter = Counter(start=1, end=10)
counter.increment()
counter.increment()
print(counter.current)  # Output: 3

counter.reset()
print(counter.current)  # Output: 1
```

#### `has_reached_end() -> bool`

Check if the counter has reached its end value.

**Returns:** `bool` - `True` if the counter is at the end value, `False` otherwise.

**Example:**

```python
counter = Counter(start=1, end=3)
print(counter.has_reached_end())  # Output: False

counter.increment()
counter.increment()
print(counter.has_reached_end())  # Output: True
```

## Usage Examples

### Basic Usage

```python
from src.counter import Counter

# Create a counter from 1 to 10
counter = Counter()

# Increment and check value
counter.increment()
print(f"Current value: {counter.current}")  # Output: Current value: 2

# Check if end is reached
if not counter.has_reached_end():
    counter.increment()

# Reset to start
counter.reset()
print(f"After reset: {counter.current}")  # Output: After reset: 1
```

### Custom Range Counter

```python
from src.counter import Counter

# Create a countdown-style counter
counter = Counter(start=10, end=20)

while not counter.has_reached_end():
    print(f"Count: {counter.current}")
    counter.increment()

print(f"Final count: {counter.current}")
```

### Safe Incrementation Pattern

```python
from src.counter import Counter

counter = Counter(start=1, end=5)

# Safe increment with boundary checking
def safe_increment(counter: Counter) -> bool:
    """Increment counter if possible, return success status."""
    if not counter.has_reached_end():
        counter.increment()
        return True
    return False

while safe_increment(counter):
    print(f"Incremented to: {counter.current}")
```

### Error Handling

```python
from src.counter import Counter

counter = Counter(start=1, end=3)

# Increment to end
counter.increment()
counter.increment()

# Attempt to exceed boundary
try:
    counter.increment()
except ValueError as e:
    print(f"Boundary reached: {e}")
    counter.reset()
    print(f"Counter reset to: {counter.current}")
```

## Thread Safety

The `Counter` class is **not thread-safe**. If you need to use a counter across multiple threads, you should implement your own synchronization mechanism using locks or other concurrency primitives.

**Example with threading lock:**

```python
import threading
from src.counter import Counter

counter = Counter(start=1, end=100)
lock = threading.Lock()

def safe_increment():
    with lock:
        if not counter.has_reached_end():
            counter.increment()
            return counter.current
    return None
```

## Edge Cases

### Single Value Counter

```python
counter = Counter(start=5, end=5)
print(counter.has_reached_end())  # Output: True
# Cannot increment at all - already at end
```

### Negative Range

```python
counter = Counter(start=-5, end=-1)
print(counter.current)  # Output: -5
counter.increment()
print(counter.current)  # Output: -4
```

### Large Range

```python
# Python handles large integers natively
counter = Counter(start=0, end=1000000)
```

## Best Practices

1. **Always check boundaries**: Use `has_reached_end()` before incrementing to avoid exceptions in production code.

2. **Reset when needed**: Call `reset()` to reuse the same counter instance instead of creating new ones.

3. **Validate inputs**: The constructor validates that `start <= end`, but ensure you pass appropriate integer values.

4. **Handle exceptions**: Wrap increment operations in try-except blocks when boundary conditions are uncertain.

5. **Use type hints**: The Counter class is fully typed; leverage this in your own code for better IDE support and type checking.

## See Also

- [README.md](../README.md) - Project overview and quick start guide
- [Unit Tests](../tests/test_counter.py) - Comprehensive unit test examples
- [BDD Scenarios](../tests/features/counter.feature) - Behavior-driven test scenarios