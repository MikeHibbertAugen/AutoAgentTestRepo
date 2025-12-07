# Error Handling and User Feedback System

## Overview

This document describes the error handling patterns and user feedback system implemented in the text-based adventure game. The system provides clear, actionable feedback for all user interactions, handles edge cases gracefully, and ensures a smooth user experience.

## Architecture

### Component Overview

The error handling system consists of three main components:

1. **Command Processor** (`src/command_processor.py`)
   - Normalizes user input (case-insensitive, whitespace trimming)
   - Parses commands and arguments
   - Validates commands against known command registry

2. **Feedback Messages** (`src/feedback_messages.py`)
   - Centralized message templates
   - Consistent formatting functions
   - Easy customization and localization support

3. **Game Engine** (`src/game_engine.py`)
   - Orchestrates command processing
   - Manages game state
   - Returns appropriate feedback messages

## Command Processing Flow

```
User Input
    ↓
normalize_command() - Trim whitespace, convert to lowercase
    ↓
parse_command() - Extract command and arguments
    ↓
is_valid_command() - Validate against command registry
    ↓
process_command() - Route to appropriate handler
    ↓
Feedback Message - Success or error message returned
```

## Error Handling Patterns

### 1. Input Normalization

All user input is normalized before processing to handle variations:

```python
# Handles: "  NORTH  ", "North", "north", " north"
normalized = normalize_command(user_input)
# Result: "north"
```

**Benefits:**
- Case-insensitive command recognition
- Whitespace tolerance (leading, trailing, multiple spaces)
- Consistent internal representation

### 2. Command Validation

Commands are validated against a registry of known commands:

```python
VALID_COMMANDS = {
    'north', 'south', 'east', 'west',
    'n', 's', 'e', 'w',
    'help', 'look', 'inventory'
}
```

**Error Response:**
- Unrecognized commands trigger helpful error message
- Suggests using 'help' command
- Does not crash or throw exceptions

### 3. Exit Validation

Movement commands are validated against available exits:

```python
if not current_location.has_exit(direction):
    return format_invalid_direction_message(direction)
```

**Error Response:**
- Clear message indicating the direction is not available
- Does not change player position
- Maintains game state consistency

## Feedback Messages

### Success Messages

**Movement Success:**
```
You move north to Huapai.
```

**Format:** `"You move {direction} to {location_name}."`

### Error Messages

**Invalid Direction:**
```
You cannot go north from here.
```

**Format:** `"You cannot go {direction} from here."`

**Unrecognized Command:**
```
I don't understand that command. Type 'help' for available commands.
```

**Format:** Fixed message with help suggestion

### Help Text

**Help Command Response:**
```
Available commands:
- Movement: north, south, east, west (or n, s, e, w)
- Information: look, help
- Inventory: inventory
```

## Extension Points

### Adding New Commands

1. Add command to `VALID_COMMANDS` registry in `command_processor.py`:
```python
VALID_COMMANDS = {
    # ... existing commands ...
    'take',
    'drop',
    'use'
}
```

2. Add handler in `game_engine.py`:
```python
def process_command(self, command: str) -> str:
    normalized = normalize_command(command)
    cmd, args = parse_command(normalized)
    
    if cmd in ['take']:
        return self.take_item(args[0] if args else None)
    # ... other handlers ...
```

3. Add feedback messages in `feedback_messages.py`:
```python
ITEM_TAKEN_MESSAGE = "You take the {item_name}."
ITEM_NOT_FOUND_MESSAGE = "There is no {item_name} here."
```

### Customizing Messages

All messages are defined as constants in `feedback_messages.py`. To customize:

1. Locate the message constant (e.g., `INVALID_DIRECTION_MESSAGE`)
2. Modify the template string
3. Ensure format placeholders match function parameters

Example:
```python
# Current
INVALID_DIRECTION_MESSAGE = "You cannot go {direction} from here."

# Customized
INVALID_DIRECTION_MESSAGE = "The path to the {direction} is blocked."
```

### Localization Support

For multi-language support:

1. Create separate message modules (e.g., `feedback_messages_es.py`)
2. Use a configuration setting to select active message module
3. Import messages dynamically based on user preference

```python
# Example approach
import importlib

language = config.get('language', 'en')
messages = importlib.import_module(f'feedback_messages_{language}')
```

## Best Practices

### 1. Always Validate Before Action

```python
# Good
if not is_valid_command(command):
    return UNRECOGNIZED_COMMAND_MESSAGE

# Bad - action before validation
self.current_location = new_location
if not is_valid_command(command):
    return "Error"  # Too late!
```

### 2. Provide Actionable Feedback

```python
# Good - tells user what to do
"I don't understand that command. Type 'help' for available commands."

# Bad - not helpful
"Error: Invalid input"
```

### 3. Maintain State Consistency

```python
# Good - only change state on success
if self.current_location.has_exit(direction):
    self.current_location = new_location
    return success_message
else:
    return error_message  # State unchanged

# Bad - state changes on error
self.current_location = new_location
if not valid:
    return error_message  # Oops, already moved!
```

### 4. Use Type Hints

```python
def move(self, direction: str) -> str:
    """Move player in specified direction."""
    # Implementation
```

Benefits:
- Better IDE support
- Catches type errors early
- Serves as documentation

## Testing Strategies

### Unit Testing

Test each component in isolation:

```python
def test_normalize_command_whitespace():
    assert normalize_command("  north  ") == "north"

def test_invalid_direction_message():
    message = format_invalid_direction_message("north")
    assert "cannot go north" in message
```

### Integration Testing

Test complete flows:

```python
def test_move_with_invalid_direction():
    game = GameEngine(start_location)
    result = game.process_command("north")
    assert "cannot go" in result
    assert game.current_location == start_location  # Unchanged
```

### Edge Cases to Test

- Empty string input: `""`
- Whitespace only: `"   "`
- Very long input: `"n" * 1000`
- Special characters: `"north!@#$"`
- Multiple spaces: `"north    south"`
- Mixed case variations: `"NoRtH"`, `"NORTH"`, `"nOrTh"`

## Security Considerations

### Input Validation

- All input is validated before processing
- Command registry prevents injection attacks
- No `eval()` or dynamic code execution

### State Protection

- Game state changes only on successful validation
- No direct state manipulation from user input
- Rollback not needed due to validation-first approach

### Data Sanitization

- Whitespace trimming prevents parsing issues
- Case normalization prevents case-sensitivity exploits
- Length limits can be added if needed

## Performance Considerations

- Command validation is O(1) using set lookup
- String normalization is O(n) where n is input length
- No regex patterns (fast processing)
- Minimal memory footprint

## Future Enhancements

1. **Command History** - Track previous commands for "undo" functionality
2. **Command Aliases** - Support user-defined shortcuts
3. **Contextual Help** - Provide location-specific command suggestions
4. **Verbose/Brief Modes** - Toggle message detail level
5. **Color-Coded Messages** - Visual distinction between success/error
6. **Sound Effects** - Audio feedback for actions
7. **Auto-Complete** - Suggest commands as user types

## Troubleshooting

### Common Issues

**Problem:** Commands not recognized after normalization
- **Solution:** Check `VALID_COMMANDS` registry includes normalized form

**Problem:** Error messages not displaying correctly
- **Solution:** Verify format placeholders match function parameters

**Problem:** State inconsistency after error
- **Solution:** Ensure validation occurs before state changes

### Debug Mode

Add logging for troubleshooting:

```python
import logging

logger = logging.getLogger(__name__)

def process_command(self, command: str) -> str:
    logger.debug(f"Processing command: {command}")
    normalized = normalize_command(command)
    logger.debug(f"Normalized to: {normalized}")
    # ... rest of processing
```

## References

- Command Pattern: https://refactoring.guru/design-patterns/command
- Input Validation Best Practices: OWASP Input Validation Cheat Sheet
- User Feedback Design: Nielsen Norman Group Usability Guidelines