import pytest
from src.location import Location
from src.location_display import LocationDisplay
from src.player import Player
from src.game_controller import GameController


class TestGameController:
    """Unit tests for GameController class."""

    @pytest.fixture
    def village_square(self):
        """Create a village square location with exits."""
        return Location(
            name="Village Square",
            description="A bustling village square with a fountain in the center.",
            exits={"north": "Market", "east": "Inn"}
        )

    @pytest.fixture
    def market(self):
        """Create a market location."""
        return Location(
            name="Market",
            description="A busy marketplace filled with vendors.",
            exits={"south": "Village Square", "west": "Bakery"}
        )

    @pytest.fixture
    def trapped_room(self):
        """Create a location with no exits."""
        return Location(
            name="Trapped Room",
            description="A small room with no visible exits.",
            exits={}
        )

    @pytest.fixture
    def locations(self, village_square, market, trapped_room):
        """Create a dictionary of all locations."""
        return {
            "Village Square": village_square,
            "Market": market,
            "Trapped Room": trapped_room
        }

    @pytest.fixture
    def player(self, village_square):
        """Create a player starting at village square."""
        return Player(village_square)

    @pytest.fixture
    def game_controller(self, player, locations):
        """Create a game controller with player and locations."""
        return GameController(player, locations)

    def test_initialization(self, game_controller, player, locations):
        """Test GameController initializes with player and locations."""
        assert game_controller.player == player
        assert game_controller.locations == locations
        assert isinstance(game_controller.display, LocationDisplay)

    def test_handle_look_command(self, game_controller):
        """Test handle_look_command returns current location information."""
        result = game_controller.handle_look_command()
        
        assert "Village Square" in result
        assert "A bustling village square with a fountain in the center." in result
        assert "north" in result
        assert "east" in result

    def test_handle_look_command_with_no_exits(self, player, trapped_room, locations):
        """Test handle_look_command for location with no exits."""
        player_trapped = Player(trapped_room)
        controller = GameController(player_trapped, locations)
        
        result = controller.handle_look_command()
        
        assert "Trapped Room" in result
        assert "A small room with no visible exits." in result
        assert "no obvious exits" in result

    def test_handle_move_command_valid_destination(self, game_controller, market):
        """Test handle_move_command moves player to valid destination."""
        result = game_controller.handle_move_command("Market")
        
        # Player should now be at Market
        assert game_controller.player.get_current_location() == market
        
        # Result should contain Market information
        assert "Market" in result
        assert "A busy marketplace filled with vendors." in result

    def test_handle_move_command_updates_location(self, game_controller, village_square, market):
        """Test handle_move_command properly updates player location."""
        # Start at Village Square
        assert game_controller.player.get_current_location() == village_square
        
        # Move to Market
        game_controller.handle_move_command("Market")
        assert game_controller.player.get_current_location() == market
        
        # Move back to Village Square
        game_controller.handle_move_command("Village Square")
        assert game_controller.player.get_current_location() == village_square

    def test_look_around_alias(self, game_controller):
        """Test look_around is an alias for handle_look_command."""
        look_result = game_controller.handle_look_command()
        around_result = game_controller.look_around()
        
        assert look_result == around_result

    def test_look_around_returns_formatted_location(self, game_controller):
        """Test look_around returns properly formatted location information."""
        result = game_controller.look_around()
        
        assert "Village Square" in result
        assert "A bustling village square with a fountain in the center." in result
        assert "Exits:" in result or "exits" in result.lower()

    def test_multiple_sequential_moves(self, game_controller, market):
        """Test multiple sequential move commands."""
        # Move to Market
        result1 = game_controller.handle_move_command("Market")
        assert "Market" in result1
        assert game_controller.player.get_current_location() == market
        
        # Move to Village Square
        result2 = game_controller.handle_move_command("Village Square")
        assert "Village Square" in result2
        
        # Look around to verify location
        result3 = game_controller.look_around()
        assert "Village Square" in result3

    def test_look_command_after_move(self, game_controller):
        """Test look command shows correct location after moving."""
        # Move to Market
        game_controller.handle_move_command("Market")
        
        # Look around
        result = game_controller.handle_look_command()
        
        # Should show Market, not Village Square
        assert "Market" in result
        assert "A busy marketplace filled with vendors." in result
        assert "Village Square" not in result or "Exits:" in result  # Name might appear in exits

    def test_game_controller_with_empty_location_dict(self, player):
        """Test GameController can be initialized with empty locations dict."""
        controller = GameController(player, {})
        assert controller.locations == {}
        
        # Should still be able to look at current location
        result = controller.look_around()
        assert "Village Square" in result

    def test_game_controller_preserves_location_state(self, game_controller, village_square):
        """Test that GameController doesn't modify location objects."""
        original_exits = village_square.get_exits()
        
        # Perform operations
        game_controller.look_around()
        game_controller.handle_look_command()
        
        # Location should remain unchanged
        assert village_square.get_exits() == original_exits
        assert village_square.name == "Village Square"