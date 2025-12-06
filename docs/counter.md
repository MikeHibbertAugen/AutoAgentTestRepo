# Counter Class Documentation

## Overview

The `Counter` class provides a simple counter implementation with automatic initialization and a maximum value constraint. The counter starts at 1 and can be incremented up to a maximum value of 10.

## Purpose

This class is designed for scenarios where you need a bounded counter that:
- Starts from a known initial value (1)
- Increments by single units
- Prevents exceeding a predefined maximum threshold
- Provides feedback when the maximum is reached

## API Reference

### Class Constants

#### `MAX_VALUE`
```python
MAX_VALUE: int = 10
```
The maximum value the counter can reach. Attempts to increment beyond this value will be rejected.

### Methods

#### `__init__(self) -> None`
Initializes a new Counter instance.

**Parameters:**
- None

**Returns:**
- None

**Behavior:**
- Sets the internal counter value to 1
- No parameters required

**Example:**
```python
counter = Counter()
# counter starts at value 1
```

---

#### `increment(self) -> bool`
Increments the counter by 1 if not at maximum value.

**Parameters:**
- None

**Returns:**
- `bool`: `True` if the counter was successfully incremented, `False` if the counter is already at `MAX_VALUE`

**Behavior:**
- If current value < `MAX_VALUE`: increments value by 1 and returns `True`
- If current value == `MAX_VALUE`: does not modify value and returns `False`

**Example:**
```python
counter = Counter()
result = counter.increment()  # Returns True, counter is now 2
result = counter.increment()  # Returns True, counter is now 3
```

---

#### `get_value(self) -> int`
Returns the current value of the counter.

**Parameters:**
- None

**Returns:**
- `int`: The current counter value

**Example:**
```python
counter = Counter()
current = counter.get_value()  # Returns 1
counter.increment()
current = counter.get_value()  # Returns 2
```

## Usage Examples

### Basic Usage
```python
from src.counter import Counter

# Create a new counter
counter = Counter()
print(counter.get_value())  # Output: 1

# Increment the counter
counter.increment()
print(counter.get_value())  # Output: 2
```

### Multiple Increments
```python
counter = Counter()

# Increment multiple times
for _ in range(5):
    counter.increment()

print(counter.get_value())  # Output: 6
```

### Handling Maximum Value
```python
counter = Counter()

# Increment to maximum
for _ in range(9):
    counter.increment()

print(counter.get_value())  # Output: 10

# Try to increment beyond maximum
result = counter.increment()
print(result)                # Output: False
print(counter.get_value())   # Output: 10 (unchanged)
```

### Checking Increment Success
```python
counter = Counter()

# Increment and check result
while counter.increment():
    print(f"Counter: {counter.get_value()}")

print(f"Maximum reached: {counter.get_value()}")
# Output shows increments from 2 to 10, then confirms maximum
```

## Boundary Behavior

### Initial State
- Counter initializes to value `1`
- First increment changes value to `2`

### Normal Operation
- Values from `1` to `9`: `increment()` returns `True` and increases value
- Counter can be incremented until reaching `MAX_VALUE` (10)

### Maximum Value
- When counter reaches `10`: `increment()` returns `False`
- Value remains at `10` regardless of additional increment attempts
- No exceptions are raised when attempting to exceed maximum

### Edge Cases
- **At value 9**: Next increment succeeds and returns `True`, setting value to 10
- **At value 10**: All subsequent increments fail and return `False`
- **Multiple attempts at maximum**: Counter remains stable at 10

## Type Hints

All methods include complete type hints for parameters and return values:
- `__init__() -> None`
- `increment() -> bool`
- `get_value() -> int`

Internal attributes are also typed:
- `_value: int` (private attribute)

## Thread Safety

**Note:** This implementation is not thread-safe. If you need to use the Counter class in a multi-threaded environment, you should implement external synchronization mechanisms (e.g., locks).