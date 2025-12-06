# Movement System Architecture

## Overview

The movement system enables players to navigate between locations in a text-based adventure game using cardinal directions (north, south, east, west) and their abbreviations (n, s, e, w).

## Architecture

### Components

#### 1. Location (`src/location.py`)
Represents a game location with named exits to other locations.

**Responsibilities:**
- Store location name
- Manage exits to neighboring locations
- Validate available directions
- Provide exit destinations

#### 2. Player (`src/player.py`)
Tracks the player's current position in the game world.

**Responsibilities:**
- Maintain current location reference
- Update location when moving

#### 3. MoveCommand (`src/movement.py`)
Processes and executes movement commands.

**Responsibilities:**
- Normalize direction input (handle abbreviations)
- Validate movement requests
- Execute valid movements
- Generate appropriate feedback messages

#### 4. Constants (`src/constants.py`)
Defines direction constants and message templates.

**Responsibilities:**
- Cardinal direction definitions
- Abbreviation mappings
- Standard message formats

## Movement Flow

1. Player issues movement command (e.g., "north", "n")
2. MoveCommand normalizes direction (converts abbreviations)
3. MoveCommand validates exit exists at current location
4. If valid: Player location updated, success message returned
5. If invalid: Player location unchanged, error message returned

## Usage Example

```python
from src.location import Location
from src.player import Player
from src.movement import MoveCommand

# Create locations
kumeu = Location("Kumeu")
huapai = Location("Huapai")

# Define exits
kumeu.add_exit("north", huapai)
huapai.add_exit("south", kumeu)

# Create player at starting location
player = Player(kumeu)

# Execute movement
result = MoveCommand.execute(player, "north")
# result.success == True
# player.current_location == huapai

# Try invalid movement
result = MoveCommand.execute(player, "east")
# result.success == False
# player.current_location == huapai (unchanged)
```

## Extension Points

The system is designed to accommodate future enhancements:

- **Additional Directions**: Add northeast, northwest, up, down to constants and Location class
- **Movement Restrictions**: Add validation logic in MoveCommand (locked doors, required items)
- **Location Events**: Trigger events when entering/leaving locations
- **Movement Costs**: Track stamina, time, or other resources
- **Dynamic Exits**: Allow exits to change based on game state

## Testing

The system includes comprehensive testing:

- **Unit Tests**: Individual component validation
- **Integration Tests**: BDD-style scenario testing matching feature requirements
- **Coverage Target**: >90% code coverage