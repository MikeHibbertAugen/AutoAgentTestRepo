# Counter Display and Output Features

## Overview
The Counter class provides methods to retrieve, display, and format counter values in various ways. This document describes the display and output functionality available in the Counter class.

## Methods

### `get_all_values()` → list[int]
Returns a list containing all counter values from start to end (inclusive).

**Returns:** List of integers representing the complete counter sequence.

**Example:**
```python
from src.counter import Counter

counter = Counter(1, 10)
values = counter.get_all_values()
print(values)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### `get_current_value()` → int
Returns the current value of the counter based on its internal position.

**Returns:** Integer representing the current counter value.

**Example:**
```python
counter = Counter(1, 10)
current = counter.get_current_value()
print(current)  # Output: 1 (or current position)
```

### `display_current()` → None
Prints the current counter value to stdout.

**Returns:** None

**Example:**
```python
counter = Counter(1, 10)
counter.display_current()  # Output: 5 (if current position is 5)
```

### `print_all()` → None
Prints each counter value on a separate line to stdout.

**Returns:** None

**Example:**
```python
counter = Counter(1, 10)
counter.print_all()
# Output:
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
```

### `to_string()` → str
Returns counter values formatted as a comma-separated string.

**Returns:** String with values separated by comma and space (", ").

**Example:**
```python
counter = Counter(1, 10)
result = counter.to_string()
print(result)  # Output: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
```

## Usage Scenarios

### Scenario 1: Retrieving All Values as a List
```python
counter = Counter(1, 10)
values = counter.get_all_values()
# Use the list for further processing
for value in values:
    # Process each value
    pass
```

### Scenario 2: Displaying Current Value
```python
counter = Counter(1, 10)
# Advance counter to desired position
counter.display_current()  # Prints current value
```

### Scenario 3: Printing All Values Sequentially
```python
counter = Counter(1, 10)
counter.print_all()  # Prints all values, one per line
```

### Scenario 4: Getting Formatted String Output
```python
counter = Counter(1, 10)
formatted = counter.to_string()
print(f"Counter values: {formatted}")
# Output: Counter values: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
```

## Formatting Conventions

- **List output**: Standard Python list format with square brackets
- **String output**: Values separated by comma followed by single space (", ")
- **Line-separated output**: Each value on its own line with newline character (\n)
- **Current value output**: Single value printed without additional formatting

## Performance Considerations

### Memory Usage
The `get_all_values()` method creates a list containing all counter values. For large ranges, this may consume significant memory:
- Range of 1-1000: ~8KB
- Range of 1-1000000: ~8MB

**Recommendation:** For very large ranges (>1 million values), consider iterating through the counter rather than creating a complete list.

### Alternative for Large Ranges
```python
counter = Counter(1, 1000000)
# Instead of: values = counter.get_all_values()
# Use iteration to avoid memory overhead
```

## Return Types and Type Hints

All methods include proper type hints:
- `get_all_values() -> list[int]`
- `get_current_value() -> int`
- `display_current() -> None`
- `print_all() -> None`
- `to_string() -> str`

## Error Handling

Methods assume the Counter has been properly initialized. Ensure the Counter object is created with valid start and end values before calling display methods.