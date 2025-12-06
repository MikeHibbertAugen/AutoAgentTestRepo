# Counter Design Documentation

## Overview
This document describes the design and implementation of a simple Counter class that provides basic counting functionality with a defined maximum value.

## Design Goals
- **Simplicity**: Provide a straightforward interface for counting operations
- **Type Safety**: Use Python type hints for clear method signatures
- **Testability**: Design with unit testing in mind
- **Maintainability**: Clear, well-documented code following Python best practices

## Class Structure

### Counter Class
The `Counter` class encapsulates counting behavior with the following characteristics:

- **Initial State**: Counter starts at value 1
- **Maximum Value**: Counter has a maximum value of 10
- **Immutable Maximum**: The maximum value is defined as a class constant

## Implementation Details

### Attributes
- `_value` (private): Internal storage for the current counter value (integer)
- `MAX_VALUE` (class constant): Maximum allowed value set to 10

### Methods

#### `__init__(self) -> None`
- Initializes the counter with a starting value of 1
- No parameters required
- Sets the internal `_value` attribute

#### `increment(self) -> None`
- Increases the counter value by 1
- No parameters required
- Does not return a value (void method)
- Simple increment operation: `_value += 1`

#### `get_value(self) -> int`
- Returns the current counter value
- No parameters required
- Returns an integer representing the current count
- Read-only access to internal state

## Design Decisions

### Starting at 1 Instead of 0
The counter initializes at 1 rather than 0 to match the business requirements. This is a domain-specific decision that may represent counting iterations, attempts, or sequential operations where the first occurrence is "1" rather than "0".

### Maximum Value Constraint
The `MAX_VALUE` constant of 10 establishes an upper bound for the counter. This constraint:
- Provides a clear business rule for counter behavior
- Can be used in validation logic if needed
- Serves as documentation for expected counter range

### Private Internal State
The `_value` attribute uses a single underscore prefix to indicate it's intended for internal use only. This encapsulation:
- Prevents direct manipulation of the counter value
- Ensures all modifications go through the `increment()` method
- Provides a clear public API through `get_value()`

### Method Naming Convention
- `increment()`: Clear, action-oriented verb indicating the operation
- `get_value()`: Explicit getter following the "get_" prefix convention for retrieving state

## Testing Strategy
The design supports comprehensive unit testing:
- Initialization can be verified by creating an instance and checking `get_value()`
- Increment behavior can be tested with sequential calls
- Maximum value scenarios can be validated
- All methods have predictable, deterministic behavior

## Future Enhancements
Potential extensions to consider:
- Add `decrement()` method for bidirectional counting
- Implement maximum value enforcement (prevent incrementing beyond MAX_VALUE)
- Add `reset()` method to return counter to initial state
- Support custom starting values through constructor parameters
- Add minimum value constraint

## Code Quality
The implementation follows:
- PEP 8 style guidelines
- Type hints for all public methods
- Comprehensive docstrings with parameter and return value documentation
- Single Responsibility Principle (class only handles counting)