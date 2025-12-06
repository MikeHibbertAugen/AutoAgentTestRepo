# Game Loop Architecture

## Overview

The game loop is the core execution engine of the text adventure game. It manages the continuous cycle of displaying game state, accepting player input, processing commands, and updating the game world. The loop runs until the player explicitly exits or interrupts execution.

## Architecture

### Components

#### GameState (`src/game_state.py`)
Manages the current state of the game including:
- Running status (is the game actively running?)
- Current location tracking
- Game initialization state

#### GameLoop (`src/game_loop.py`)
Controls the main execution flow:
- Displays current location to player
- Reads and processes player commands
- Handles graceful exits
- Manages game lifecycle

## Game Loop Flow

```
┌─────────────────────────────────────────┐
│         Initialize Game State           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      Display Initial Location           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Wait for Input │
         └────────┬─────────┘
                  │
                  ▼
         ┌─────────────────┐
    ┌────│ Process Command │────┐
    │    └─────────────────┘    │
    │                            │
    ▼                            ▼
┌────────┐              ┌──────────────┐
│  Quit? │───No────────▶│ Execute Cmd  │
└───┬────┘              └──────┬───────┘
    │                          │
   Yes                         │
    │                          │
    │         ┌────────────────┘
    │         │
    ▼         ▼
┌──────────────────┐
│ Display Farewell │
└──────────────────┘
```

## Command Processing Lifecycle

### 1. Input Reception
- Game loop waits for player input using `input()` function
- Input is captured as a raw string

### 2. Command Parsing
- Command string is processed by command processor
- Commands are normalized (lowercase, trimmed whitespace)

### 3. Command Execution
- Special commands (`quit`, `exit`) handled by game loop directly
- Other commands delegated to command handlers (future implementation)
- Command execution may modify game state

### 4. State Update
- Game state updated based on command results
- Location changes, inventory updates, etc.

### 5. Output Display
- Results of command execution displayed to player
- New location descriptions shown if applicable

## Exit Strategies

The game loop supports three methods for graceful exit:

### 1. Quit Command
```
> quit
```
- Explicit exit command
- Displays farewell message
- Cleanly terminates game loop

### 2. Exit Command
```
> exit
```
- Alternative explicit exit command
- Same behavior as `quit`
- Provides user flexibility

### 3. Keyboard Interrupt (Ctrl+C)
```
> ^C
```
- Handles `KeyboardInterrupt` exception
- Displays farewell message
- Ensures cleanup occurs

All exit methods:
- Set `game_state.is_running = False`
- Display farewell message
- Allow cleanup operations
- Exit gracefully without errors

## Usage Examples

### Basic Game Loop Initialization

```python
from src.game_state import GameState
from src.game_loop import GameLoop

# Initialize game components
game_state = GameState()
game_loop = GameLoop(game_state)

# Start the game
game_loop.run()
```

### Custom Game Loop with Location

```python
game_state = GameState()
game_state.set_current_location("You are standing in a dark forest.")

game_loop = GameLoop(game_state)
game_loop.run()
```

### Testing with Mock Input

```python
from unittest.mock import patch

def test_game_commands():
    game_state = GameState()
    game_loop = GameLoop(game_state)
    
    # Simulate command sequence
    with patch('builtins.input', side_effect=['look', 'north', 'quit']):
        game_loop.run()
```

## Extension Points

The game loop is designed for extensibility:

### Adding New Commands

Future command handlers can be registered with the command processor:

```python
# Future implementation
command_processor.register('look', look_handler)
command_processor.register('inventory', inventory_handler)
command_processor.register('take', take_handler)
```

### Custom Exit Handlers

Exit behavior can be customized by overriding `display_farewell()`:

```python
class CustomGameLoop(GameLoop):
    def display_farewell(self):
        print("Thanks for playing! Your score: 100")
```

### State Persistence

Game state can be saved before exit:

```python
def process_command(self, command: str) -> bool:
    if command in ['quit', 'exit']:
        self.save_game()  # Future implementation
        return False
    return True
```

### Pre/Post Command Hooks

Commands can trigger before/after hooks:

```python
def process_command(self, command: str) -> bool:
    self.before_command(command)  # Hook
    result = self.execute_command(command)
    self.after_command(command, result)  # Hook
    return result
```

## Error Handling

### Input Errors
- Empty input: Display prompt again
- Invalid commands: Show help message
- Malformed input: Graceful error message

### System Errors
- `KeyboardInterrupt`: Caught and handled gracefully
- `EOFError`: Treated as exit command
- Other exceptions: Logged and displayed to user

## Performance Considerations

- Loop runs synchronously (blocking input)
- No significant memory accumulation
- Game state remains lightweight
- Command processing is O(1) for lookups

## Future Enhancements

1. **Command History**: Track previous commands for undo/replay
2. **Auto-save**: Periodic state persistence
3. **Scripting**: Support command files for testing/automation
4. **Async Input**: Non-blocking input for real-time events
5. **Plugin System**: Dynamic command handler registration
6. **Debug Mode**: Enhanced logging and state inspection

## Testing

### Unit Tests
- Test individual methods in isolation
- Mock dependencies (input/output)
- Verify state transitions

### Integration Tests
- Test complete command sequences
- Verify end-to-end flow
- Test all exit paths

### BDD Tests
- Scenario-based testing
- User story validation
- Acceptance criteria verification

## Related Documentation

- `src/game_state.py` - Game state implementation details
- `src/game_loop.py` - Game loop implementation details
- `tests/test_game_loop.py` - BDD test scenarios