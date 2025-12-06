# Console Commands Reference

## Overview

This document provides a comprehensive guide to all available commands in the text-based adventure game. Commands are used to interact with the game world, navigate between locations, and control the game.

## Command Categories

### Movement Commands

Movement commands allow you to travel between locations in the game world.

#### Full Movement Commands

Use the `go` keyword followed by a direction:

- `go north` - Move to the location to the north
- `go south` - Move to the location to the south
- `go east` - Move to the location to the east
- `go west` - Move to the location to the west

**Examples:**
```
[Helensville] > go north
[Market Square] > go east
[Town Hall] > go south
```

#### Abbreviated Movement Commands

For faster navigation, use single-letter direction shortcuts:

- `n` - Move north
- `s` - Move south
- `e` - Move east
- `w` - Move west

**Examples:**
```
[Helensville] > n
[Market Square] > e
[Town Hall] > s
```

### Information Commands

#### Look Command

Use `look` to examine your current surroundings and get a detailed description of your location.

**Syntax:** `look`

**Example:**
```
[Helensville] > look
You are in Helensville, a small town surrounded by rolling hills...
```

#### Help Command

Use `help` to display available commands and basic instructions.

**Syntax:** `help`

**Example:**
```
[Helensville] > help
Available commands:
  Movement: go [direction] or n/s/e/w
  Information: look, help
  Game: quit
```

### Game Control Commands

#### Quit Command

Use `quit` to exit the game.

**Syntax:** `quit`

**Example:**
```
[Helensville] > quit
Thanks for playing! Goodbye.
```

## Command Syntax Reference

| Command | Aliases | Arguments | Description |
|---------|---------|-----------|-------------|
| `go north` | `n` | none | Move to the northern location |
| `go south` | `s` | none | Move to the southern location |
| `go east` | `e` | none | Move to the eastern location |
| `go west` | `w` | none | Move to the western location |
| `look` | - | none | Examine current location |
| `help` | - | none | Display help information |
| `quit` | - | none | Exit the game |

## Command Features

### Case Insensitivity

All commands are case-insensitive. The following are all equivalent:

- `go north`
- `Go North`
- `GO NORTH`
- `gO nOrTh`

### Whitespace Handling

Extra whitespace is automatically trimmed from commands:

- `   go north   ` is treated as `go north`
- `look   ` is treated as `look`

### Empty Input

Pressing Enter without typing a command will simply redisplay the prompt without any error message.

## Tips for New Players

1. **Use abbreviated commands** - Save time by using `n`, `s`, `e`, `w` instead of full movement commands
2. **Look around** - Use `look` frequently to get descriptions and clues about your surroundings
3. **Case doesn't matter** - Type commands in whatever case is most comfortable for you
4. **Try help** - If you forget a command, type `help` to see the available options
5. **Navigate efficiently** - Plan your route before moving to minimize unnecessary travel

## Error Handling

### Invalid Commands

If you enter a command that is not recognized, you'll see an error message:

```
[Helensville] > jump
Invalid command. Type 'help' for available commands.
```

### Invalid Directions

If you try to move in a direction that is not available from your current location, the game will inform you:

```
[Helensville] > go north
You cannot go north from here.
```

## Command Examples by Scenario

### Exploring a New Location

```
[Helensville] > look
You see a small town with paths leading in multiple directions.

[Helensville] > n
You move north to Market Square.

[Market Square] > look
The bustling market square is filled with merchants and shoppers.
```

### Getting Help

```
[Town Hall] > help
Available commands:
  Movement: go [direction] or n/s/e/w
  Information: look, help
  Game: quit

[Town Hall] > 
```

### Navigating Back

```
[Forest Path] > s
You move south to Helensville.

[Helensville] > e
You move east to River Crossing.

[River Crossing] > w
You move west back to Helensville.
```

### Exiting the Game

```
[Helensville] > quit
Thanks for playing! Goodbye.
```

## Frequently Asked Questions

**Q: Can I undo a movement command?**  
A: Not currently. Plan your movements carefully or navigate back manually.

**Q: Are there diagonal directions like northeast or southwest?**  
A: No, only the four cardinal directions (north, south, east, west) are supported.

**Q: What happens if I type multiple words that aren't a valid command?**  
A: The game will display an "Invalid command" message and prompt you to try again.

**Q: Can I abbreviate other commands besides directions?**  
A: Currently, only direction commands have abbreviations. Commands like `look`, `help`, and `quit` must be typed in full.

**Q: Is there a way to see my command history?**  
A: Command history depends on your terminal or console settings. Most terminals support using the up arrow key to recall previous commands.

## Future Commands

The game may be extended with additional commands in future versions, such as:

- Inventory management commands
- Object interaction commands
- Character interaction commands
- Save and load game commands

Check back for updates to this documentation as new features are added.