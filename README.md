# AutoAgentTestRepo

This is a test repository for string manipulation utilities, timezone services, a configurable counter implementation, and a text-based adventure game world location system with rich location description display.

## Features

This package provides string manipulation utilities, timezone services, a counter class, and a location-based game world system with immersive location descriptions, featuring type safety, comprehensive testing, and clean code practices.

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
from src.world_initializer import initialize_world
from src.location_display import LocationDisplay
from src.player import Player
from src.game_controller import GameController
from src.game_world import GameWorld
from src.locations_data import populate_nw_auckland_world

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

# Create game locations with exits
beach = Location("Muriwai Beach", "A beautiful black sand beach on the west coast", 
                 {"east": "Waitakere Ranges"})
forest = Location("Waitakere Ranges", "Dense native forest with walking trails",
                  {"west": "Muriwai Beach"})

# Display location information
display = LocationDisplay()
location_info = display.format_location_info(beach)
print(location_info)
# Output:
# === Muriwai Beach ===
# A beautiful black sand beach on the west coast
# Exits: east

# Initialize a complete game with player and locations
locations = {
    "Town Square": Location("Town Square", "A bustling central plaza", 
                           {"north": "Castle", "south": "Market"}),
    "Castle": Location("Castle", "An imposing stone fortress",
                      {"south": "Town Square"}),
    "Market": Location("Market", "A vibrant marketplace",
                      {"north": "Town Square"})
}
starting_location = locations["Town Square"]
player = Player(starting_location)
game = GameController(player, locations)

# Look around current location
print(game.look_around())
# Output:
# === Town Square ===
# A bustling central plaza
# Exits: north, south

# Move to a new location (automatically displays new location)
print(game.handle_move_command("Castle"))
# Output:
# === Castle ===
# An imposing stone fortress
# Exits: south

# Create and populate NW Auckland game world
world = GameWorld()
populate_nw_auckland_world(world)

# Access the starting location
start = world.starting_location
print(f"Game starts at: {start.name}")
print(f"Description: {start.description}")

# Navigate the world
current = start
for direction in current.connections.keys():
    print(f"You can go {direction}")
```

## Location Description System

A comprehensive location description system for text-based adventure games that displays immersive location information including names, descriptions, and available exits. The system automatically displays location information when players arrive and when they explicitly look around.

### Core Components

#### Location Class

The `Location` class represents individual game locations with names, descriptions, and directional exits.

**Usage:**

```python
from src.location import Location

# Create a location with exits
tavern = Location(
    name="The Prancing Pony",
    description="A cozy tavern with a roaring fireplace",
    exits={"north": "Town Square", "east": "Stables"}
)

# Create a location without exits (dead end)
treasure_room = Location(
    name="Treasure Room",
    description="A hidden chamber filled with gold and jewels"
)

# Access location properties
print(tavern.name)  # Output: The Prancing Pony
print(tavern.description)  # Output: A cozy tavern with a roaring fireplace

# Get available exit directions
exits = tavern.get_exits()
print(exits)  # Output: ['north', 'east']

# Check if location has any exits
print(tavern.has_exits())  # Output: True
print(treasure_room.has_exits())  # Output: False

# Get destination for a specific direction
destination = tavern.get_exit_destination("north")
print(destination)  # Output: Town Square
```

#### LocationDisplay Class

The `LocationDisplay` class handles formatting and displaying location information in a consistent, immersive format.

**Usage:**

```python
from src.location import Location
from src.location_display import LocationDisplay

display = LocationDisplay()

# Create a location
forest = Location(
    name="Enchanted Forest",
    description="Ancient trees tower above you, their branches forming a canopy",
    exits={"north": "Clearing", "south": "River", "west": "Cave"}
)

# Format complete location information
info = display.format_location_info(forest)
print(info)
# Output:
# === Enchanted Forest ===
# Ancient trees tower above you, their branches forming a canopy
# Exits: north, south, west

# Format individual components
name = display.format_name(forest)
description = display.format_description(forest)
exits = display.format_exits(forest)

# Handle location with no exits
dead_end = Location("Dead End", "A solid stone wall blocks your path")
info = display.format_location_info(dead_end)
print(info)
# Output:
# === Dead End ===
# A solid stone wall blocks your path
# There are no obvious exits.
```

#### Player Class

The `Player` class tracks the player's current location in the game world.

**Usage:**

```python
from src.location import Location
from src.player import Player

# Create starting location
starting_loc = Location("Village", "A peaceful village", {"north": "Forest"})

# Initialize player
player = Player(starting_loc)

# Get current location
current = player.get_current_location()
print(current.name)  # Output: Village

# Move to a new location
forest = Location("Forest", "Dense woodland", {"south": "Village"})
player.move_to(forest)
print(player.get_current_location().name)  # Output: Forest
```

#### GameController Class

The `GameController` class orchestrates the game, handling player commands and coordinating location display.

**Usage:**

```python
from src.location import Location
from src.player import Player
from src.game_controller import GameController

# Set up game world
locations = {
    "Entrance": Location("Castle Entrance", "Grand gates of the castle",
                        {"north": "Hall", "south": "Courtyard"}),
    "Hall": Location("Great Hall", "A magnificent hall with high ceilings",
                    {"south": "Entrance"}),
    "Courtyard": Location("Courtyard", "An open courtyard",
                         {"north": "Entrance"})
}

# Initialize player and game
player = Player(locations["Entrance"])
game = GameController(player, locations)

# Look around current location
print(game.handle_look_command())
# Output:
# === Castle Entrance ===
# Grand gates of the castle
# Exits: north, south

# Move to a new location (automatically shows new location)
print(game.handle_move_command("Hall"))
# Output:
# === Great Hall ===
# A magnificent hall with high ceilings
# Exits: south

# Look around again in current location
print(game.look_around())
# Output:
# === Great Hall ===
# A magnificent hall with high ceilings
# Exits: south
```

### Complete Example: Building a Mini Adventure

```python
from src.location import Location
from src.player import Player
from src.game_controller import GameController

# Create a small game world
locations = {
    "Forest Entrance": Location(
        "Forest Entrance",
        "You stand at the edge of a dark forest",
        {"north": "Deep Forest", "east": "Meadow"}
    ),
    "Deep Forest": Location(
        "Deep Forest",
        "The trees grow thick here, blocking out the sunlight",
        {"south": "Forest Entrance", "west": "Hidden Grove"}
    ),
    "Meadow": Location(
        "Sunny Meadow",
        "A bright meadow filled with wildflowers",
        {"west": "Forest Entrance"}
    ),
    "Hidden Grove": Location(
        "Hidden Grove",
        "A secret grove with a crystal-clear spring",
        {"east": "Deep Forest"}
    )
}

# Start the game
player = Player(locations["Forest Entrance"])
game = GameController(player, locations)

# Play through the game
print("=== Welcome to the Forest Adventure ===\n")

# Look around starting location
print(game.look_around())
print()

# Explore north
print("You venture north into the forest...")
print(game.handle_move_command("Deep Forest"))
print()

# Continue exploring west
print("You notice a path to the west...")
print(game.handle_move_command("Hidden Grove"))
print()

# Look around the grove
print("You examine your surroundings more carefully...")
print(game.look_around())
```

### Features

- **Automatic Location Display**: Location information is automatically shown when player arrives at a new location
- **Explicit Look Command**: Players can look around their current location at any time
- **Formatted Output**: Clean, consistent formatting with location names, descriptions, and exit lists
- **No Exit Handling**: Special message displayed for locations with no available exits (dead ends)
- **Type-Safe**: Full type hints throughout the codebase
- **Comprehensive Testing**: 100% test coverage with unit and BDD tests
- **Easy Integration**: Simple API for building text adventure games

### API Reference

**Location Class:**
- `__init__(name: str, description: str, exits: dict[str, str] = None)` - Create a location
- `get_exits() -> list[str]` - Get list of available exit directions
- `has_exits() -> bool` - Check if location has any exits
- `get_exit_destination(direction: str) -> str | None` - Get destination name for direction

**LocationDisplay Class:**
- `format_location_info(location: Location) -> str` - Format complete location information
- `format_name(location: Location) -> str` - Format location name
- `format_description(location: Location) -> str` - Format description
- `format_exits(location: Location) -> str` - Format exits list or no exit message

**Player Class:**
- `__init__(starting_location: Location)` - Initialize player at starting location
- `get_current_location() -> Location` - Get current location
- `move_to(location: Location) -> None` - Move to new location

**GameController Class:**
- `__init__(player: Player, locations: dict[str, Location])` - Initialize game
- `handle_look_command() -> str` - Handle look command, return location info
- `handle_move_command(destination_name: str) -> str` - Handle movement, return new location info
- `look_around() -> str` - Alias for looking around current location

## Game World System

A comprehensive game world management system for text-based adventure games, featuring location graphs with bidirectional connections and full connectivity analysis. The system includes authentic north-west Auckland locations for an immersive New Zealand gaming experience.

### Quick Start

```python
from src.game_world import GameWorld, Location
from src.locations_data import populate_nw_auckland_world

# Create and populate a complete NW Auckland game world
world = GameWorld()
populate_nw_auckland_world(world)

# Start exploring from Helensville
current_location = world.starting_location
print(f"You are at: {current_location.name}")
print(f"{current_location.description}")

# Check available connections
for direction, connected_loc in current_location.connections.items():
    print(f"Go {direction} to {connected_loc.name}")

# Navigate to Parakai
if "north" in current_location.connections:
    current_location = current_location.connections["north"]
    print(f"\nYou travel north to: {current_location.name}")
    print(f"{current_location.description}")
```

### Core Components

#### Location Class

Represents individual game locations with names, descriptions, and directional connections to other locations.

**Usage:**

```python
from src.game_world import Location

# Create locations
helensville = Location(
    name="Helensville",
    description="A historic town on the banks of the Kaipara River",
    is_starting=True
)

parakai = Location(
    name="Parakai",
    description="Home to natural hot springs and pools"
)

# Check starting location flag
print(helensville.is_starting)  # Output: True
print(parakai.is_starting)  # Output: False

# Add connections between locations
helensville.connections["north"] = parakai
parakai.connections["south"] = helensville

# Navigate between locations
next_location = helensville.connections.get("north")
if next_location:
    print(f"Going north to: {next_location.name}")
```

**Location API:**
- `__init__(name: str, description: str, is_starting: bool = False)` - Create a location
- `name: str` - Location name (read-only property)
- `description: str` - Location description (read-only property)
- `is_starting: bool` - Flag indicating if this is the starting location (read-only property)
- `connections: dict[str, Location]` - Dictionary mapping directions to connected locations

#### GameWorld Class

Manages the collection of all locations and provides methods for building and analyzing the game world graph.

**Usage:**

```python
from src.game_world import GameWorld, Location

# Create an empty game world
world = GameWorld()

# Add locations to the world
helensville = Location("Helensville", "A historic town", is_starting=True)
kumeu = Location("Kumeu", "The heart of Auckland's wine country")
muriwai = Location("Muriwai Beach", "A wild west coast beach")

world.add_location(helensville)
world.add_location(kumeu)
world.add_location(muriwai)

# Connect locations bidirectionally
world.connect_locations("Helensville", "Kumeu", "east")
# This creates: Helensville --east--> Kumeu AND Kumeu --west--> Helensville

world.connect_locations("Kumeu", "Muriwai Beach", "west")
# This creates: Kumeu --west--> Muriwai Beach AND Muriwai Beach --east--> Kumeu

# Access locations
location = world.get_location("Kumeu")
print(location.name)  # Output: Kumeu

# Count total locations
print(world.count_locations())  # Output: 3

# Check if world is fully connected (all locations reachable from start)
print(world.is_fully_connected())  # Output: True

# Access starting location
print(world.starting_location.name)  # Output: Helensville
```

**GameWorld API:**
- `__init__()` - Create an empty game world
- `add_location(location: Location) -> None` - Add a location to the world
- `get_location(name: str) -> Optional[Location]` - Get location by name
- `connect_locations(loc1_name: str, loc2_name: str, direction: str) -> None` - Create bidirectional connection
- `count_locations() -> int` - Get total number of locations in world
- `is_fully_connected() -> bool` - Check if all locations are reachable from starting location
- `starting_location: Optional[Location]` - Property to access the starting location
- `locations: dict[str, Location]` - Dictionary of all locations indexed by name

**Bidirectional Connection Details:**

When you call `connect_locations(loc1, loc2, direction)`, the system automatically creates both directions:
- Location 1 → Location 2 in the specified direction
- Location 2 → Location 1 in the opposite direction

Direction opposites:
- north ↔ south
- east ↔ west
- northeast ↔ southwest
- northwest ↔ southeast

### North-West Auckland Locations

The `populate_nw_auckland_world()` function creates a complete game world featuring authentic north-west Auckland locations.

**Usage:**

```python
from src.game_world import GameWorld
from src.locations_data import populate_nw_auckland_world

# Create and populate the world
world = GameWorld()
populate_nw_auckland_world(world)

# Explore from the starting location
current = world.starting_location
print(f"Starting at: {current.name}")
print(f"{current.description}")

# Navigate the world
if "north" in current.connections:
    current = current.connections["north"]
    print(f"\nTraveled north to: {current.name}")
    print(f"{current.description}")
```

**Featured Locations:**

The world includes these authentic north-west Auckland locations (8+ locations):
- **Helensville** (Starting Location) - A historic town on the banks of the Kaipara River
- **Parakai** - Home to natural hot springs and pools
- **Kumeu** - The heart of Auckland's wine country with numerous vineyards
- **Huapai** - A charming wine region village near Kumeu
- **Muriwai Beach** - A wild west coast beach famous for its gannet colony
- **Waimauku** - A rural township connecting to the coast
- **Riverhead** - A historic wharf town on the upper Waitemata Harbour
- **Coatesville** - A semi-rural area with lifestyle properties
- And more...

**Location Connections:**

The world features bidirectional connections including:
- Helensville ↔ Parakai (north/south)
- Kumeu ↔ Huapai (north/south)
- Muriwai Beach ↔ Waimauku (east/west)
- Riverhead ↔ Kumeu (connections vary)
- Riverhead ↔ Coatesville (connections vary)
- Additional connections ensuring full world connectivity

**Features:**
- Minimum 8 distinct Auckland locations
- All locations reachable from Helensville (fully connected graph)
- Authentic location descriptions matching real geography
- Bidirectional navigation between all connected locations
- Starting location clearly designated

### Complete Example

```python
from src.game_world import GameWorld
from src.locations_data import populate_nw_auckland_world

# Initialize the NW Auckland game world
world = GameWorld()
populate_nw_auckland_world(world)

print("=== Welcome to North-West Auckland Adventure ===\n")

# Verify world is properly set up
print(f"Total locations: {world.count_locations()}")
print(f"Fully connected: {world.is_fully_connected()}")
print()

# Start the game
current = world.starting_location
print(f"You begin your journey in {current.name}")
print(f"{current.description}\n")

# Show available directions
print("Available directions:")
for direction in current.connections.keys():
    destination = current.connections[direction]
    print(f"  {direction} -> {destination.name}")
print()

# Explore Parakai
if "north" in current.connections:
    current = current.connections["north"]
    print(f"You travel north to {current.name}")
    print(f"{current.description}\n")

# Return to Helensville
if "south" in current.connections:
    current = current.connections["south"]
    print(f"You travel south back to {current.name}")
    print(f"{current.description}\n")

# Explore wine country
kumeu = world.get_location("Kumeu")
if kumeu:
    print(f"You travel to {kumeu.name}")
    print(f"{kumeu.description}\n")
    
    # Visit neighboring locations
    for direction, destination in kumeu.connections.items():
        print(f"From here you can go {direction} to {destination.name}")
```

### Graph Analysis

The `is_fully_connected()` method uses breadth-first search to verify that all locations in the world can be reached from the starting location.

```python
from src.game_world import GameWorld, Location

world = GameWorld()

# Add locations
start = Location("Start", "The beginning", is_starting=True)
middle = Location("Middle", "The middle point")
end = Location("End", "The destination")
isolated = Location("Isolated", "Cannot reach this")

world.add_location(start)
world.add_location(middle)
world.add_location(end)
world.add_location(isolated)

# Connect only some locations
world.connect_locations("Start", "Middle", "north")
world.connect_locations("Middle", "End", "east")

# Check connectivity
print(world.is_fully_connected())  # Output: False (isolated location not reachable)

# Connect the isolated location
world.connect_locations("End", "Isolated", "north")
print(world.is_fully_connected())  # Output: True (all locations now reachable)
```

### API Reference

**Location Class:**
- `__init__(name: str, description: str, is_starting: bool = False)` - Create a location
- `name: str` - Location name (property)
- `description: str` - Location description (property)
- `is_starting: bool` - Starting location flag (property)
- `connections: dict[str, Location]` - Directional connections to other locations

**GameWorld Class:**
- `__init__()` - Create empty game world
- `add_location(location: Location) -> None` - Add a location to the world
- `get_location(name: str) -> Optional[Location]` - Retrieve location by name
- `connect_locations(loc1_name: str, loc2_name: str, direction: str) -> None` - Create bidirectional connection
- `count_locations() -> int` - Count total locations in world
- `is_fully_connected() -> bool` - Check if all locations reachable from start
- `starting_location: Optional[Location]` - Starting location property
- `locations: dict[str, Location]` - All locations indexed by name

**Data Module:**
- `populate_nw_auckland_world(world: GameWorld) -> None` - Populate world with NW Auckland locations

### Testing

The game world system includes comprehensive test coverage:

**Unit Tests** (`tests/test_game_world.py`):
- Location creation and properties
- GameWorld location management
- Bidirectional connection creation
- Location retrieval and counting
- Graph connectivity analysis
- Edge cases (empty world, isolated locations)

**BDD Tests** (`tests/features/test_nw_auckland_locations.bdd.py`):
- Helensville as starting location
- Kumeu wine region verification
- Muriwai Beach and coastal connections
- Parakai hot springs location
- Riverhead area connections
- Minimum 8 locations requirement
- Full world connectivity validation

Run tests:
```bash
# Run all game world tests
pytest tests/test_game_world.py -v

# Run BDD scenario tests
pytest tests/features/test_nw_auckland_locations.bdd.py -v

# Run with coverage
pytest tests/test_game_world.py tests/features/test_nw_auckland_locations.bdd.py --cov=src.game_world --cov=src.locations_data
```

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
pytest tests/test_game_world.py -v
pytest tests/