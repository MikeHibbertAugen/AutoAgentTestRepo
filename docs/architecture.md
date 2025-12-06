# Architecture Documentation

## Overview

This document describes the architecture and design decisions for the Location model in the text-based adventure game. The Location class serves as the foundational building block for creating navigable game worlds.

## Core Design Principles

### Simplicity
The Location class follows the principle of simplicity, providing only essential functionality needed to represent a place in the game world. Additional features (items, NPCs, events) can be added through composition rather than bloating the base class.

### Type Safety
All public methods and attributes use type hints to enable static type checking with mypy. This catches errors at development time rather than runtime, improving code reliability.

### Immutability Where Appropriate
Location names and descriptions are set at initialization and accessed via properties, preventing accidental modification. Exits are mutable to allow dynamic world construction.

## Class Design

### Location Class

```
Location
├── Attributes
│   ├── _name: str (private)
│   ├── _description: str (private)
│   └── _exits: Dict[str, Location] (private)
├── Properties
│   ├── name: str (read-only)
│   └── description: str (read-only)
└── Methods
    ├── add_exit(direction: str, destination: Location) -> None
    ├── get_exit(direction: str) -> Optional[Location]
    └── get_available_exits() -> List[str]
```

### Attributes

- **_name**: Private attribute storing the location's display name
- **_description**: Private attribute storing the location's descriptive text
- **_exits**: Private dictionary mapping direction strings to destination Location objects

### Methods

#### `add_exit(direction: str, destination: Location) -> None`
Adds a navigable exit from this location to another. Allows overwriting existing exits for the same direction, enabling dynamic world modification.

**Design Decision**: No validation on direction strings to allow flexibility (cardinal directions, "up", "down", custom directions like "through mirror").

#### `get_exit(direction: str) -> Optional[Location]`
Retrieves the destination location for a given direction. Returns `None` if no exit exists in that direction.

**Design Decision**: Returns `Optional[Location]` rather than raising exceptions, following the "easier to ask for forgiveness" Python pattern while still being explicit about potential None values.

#### `get_available_exits() -> List[str]`
Returns a sorted list of all available exit directions. Sorting ensures consistent output for testing and user interface display.

**Design Decision**: Returns a list rather than exposing the internal dictionary keys, maintaining encapsulation.

## Data Flow

### Location Creation
```
1. Create Location with name and optional description
2. Location stores immutable name and description
3. Empty exits dictionary initialized
```

### World Building
```
1. Create multiple Location instances
2. Connect locations using add_exit() method
3. Build navigable graph structure
```

### Navigation Flow
```
1. Player at current_location
2. Query available_exits = current_location.get_available_exits()
3. Player selects direction from available exits
4. next_location = current_location.get_exit(direction)
5. Move player to next_location if not None
```

## Design Decisions

### Exit Storage as Dictionary
**Decision**: Store exits as `Dict[str, Location]` rather than a list of tuples.

**Rationale**: Dictionary provides O(1) lookup performance and naturally prevents duplicate directions. Direction strings serve as keys, making the code self-documenting.

### No Bidirectional Exit Automation
**Decision**: Adding an exit from Location A to Location B does not automatically create a reverse exit.

**Rationale**: Many game scenarios require one-way passages (slides, locked doors, teleporters). Developers can explicitly create bidirectional connections when needed. A helper function could be added later without changing the core API.

### String-Based Directions
**Decision**: Use strings for directions rather than an enum.

**Rationale**: Maximum flexibility for custom directions. An enum could be too restrictive for creative location connections (e.g., "through portal", "into rabbit hole").

### Optional Description
**Decision**: Make description optional with empty string default.

**Rationale**: During prototyping, developers may want to create locations with just names. Descriptions can be added later. Empty string avoids None-checking in client code.

### Immutable Core Properties
**Decision**: Name and description cannot be changed after initialization.

**Rationale**: Locations represent fixed places in the game world. Changing their identity could break game logic. New locations should be created for different places.

## Extensibility Points

### Future Enhancements

1. **Location Categories/Types**
   - Add optional `location_type: str` parameter (indoor, outdoor, dungeon, shop)
   - Enable filtering and special behaviors by type

2. **Bi-directional Exit Helper**
   ```python
   def connect_locations(loc1: Location, dir1: str, loc2: Location, dir2: str) -> None:
       loc1.add_exit(dir1, loc2)
       loc2.add_exit(dir2, loc1)
   ```

3. **Exit Conditions**
   - Extend to support conditional exits (locked doors, puzzle requirements)
   - Could use callable conditions: `add_conditional_exit(direction, destination, condition_fn)`

4. **Serialization Support**
   - Add unique location IDs for save/load functionality
   - Implement `to_dict()` and `from_dict()` methods

5. **Container Functionality**
   - Add items list: `_items: List[Item]`
   - Add NPCs list: `_npcs: List[NPC]`
   - Maintain single responsibility by keeping these optional

6. **Event System**
   - Add hooks for entry/exit events
   - Enable custom behavior when player enters/leaves

### Extension via Composition

Rather than subclassing Location, consider composition for specialized behaviors:

```python
class LocationManager:
    def __init__(self, location: Location):
        self.location = location
        self.items: List[Item] = []
        self.npcs: List[NPC] = []
        self.visited: bool = False
```

This keeps the Location class focused while enabling rich functionality.

## Testing Strategy

### Unit Testing
- Test all public methods independently
- Verify immutability of name and description
- Test edge cases (empty descriptions, non-existent exits)
- Achieve 100% code coverage

### BDD Testing
- Feature files describe player-facing behavior
- Step definitions create test worlds matching game scenarios
- Ensures Location class supports actual gameplay requirements

### Type Checking
- mypy ensures type safety across all method signatures
- Catches potential None reference errors at development time

## Performance Considerations

- **Memory**: Each location stores references to connected locations. For large worlds (1000+ locations), this is minimal overhead.
- **Lookup**: Exit lookup is O(1) via dictionary access
- **Circular References**: Python's garbage collector handles circular location references, but weak references could be considered for very large graphs

## Compatibility

- **Python Version**: Requires Python 3.9+ for modern type hint syntax
- **Dependencies**: No external dependencies for core Location class
- **Platform**: Pure Python, platform-independent

## Security Considerations

Since this is a single-player game with no user-supplied code execution:
- Input validation is minimal (direction strings are user input but only used as dictionary keys)
- No SQL injection or XSS concerns
- Save file tampering possible but acceptable for single-player games

## Conclusion

The Location class provides a clean, type-safe foundation for building text adventure game worlds. Its simple API enables rapid prototyping while remaining extensible for future features through composition and optional enhancements.