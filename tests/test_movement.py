"""
Unit tests for the movement command processing module.

Tests cover:
- Direction normalization (abbreviations)
- Movement validation
- Success and error message generation
- Movement result status
"""

import pytest
from src.movement import MoveCommand, MovementResult
from src.player import Player
from src.location import Location


class TestMoveCommand:
    """Test suite for MoveCommand class."""

    @pytest.fixture
    def setup_locations(self):
        """Create test locations with connections."""
        kumeu = Location("Kumeu")
        huapai = Location("Huapai")
        muriwai = Location("Muriwai")
        
        kumeu.add_exit("north", huapai)
        kumeu.add_exit("south", muriwai)
        huapai.add_exit("south", kumeu)
        
        return kumeu, huapai, muriwai

    @pytest.fixture
    def player_at_kumeu(self, setup_locations):
        """Create a player at Kumeu location."""
        kumeu, _, _ = setup_locations
        return Player(kumeu)

    def test_move_with_full_direction_name(self, player_at_kumeu, setup_locations):
        """Test movement with full direction name (e.g., 'north')."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "north")
        
        assert result.success is True
        assert player_at_kumeu.current_location == huapai
        assert "success" in result.message.lower() or "moved" in result.message.lower()

    def test_move_with_direction_abbreviation(self, player_at_kumeu, setup_locations):
        """Test movement with direction abbreviation (e.g., 'n' for north)."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "n")
        
        assert result.success is True
        assert player_at_kumeu.current_location == huapai

    def test_move_south_with_abbreviation(self, player_at_kumeu, setup_locations):
        """Test south movement with 's' abbreviation."""
        kumeu, _, muriwai = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "s")
        
        assert result.success is True
        assert player_at_kumeu.current_location == muriwai

    def test_all_direction_abbreviations(self, setup_locations):
        """Test that all direction abbreviations work correctly."""
        center = Location("Center")
        north_loc = Location("North")
        south_loc = Location("South")
        east_loc = Location("East")
        west_loc = Location("West")
        
        center.add_exit("north", north_loc)
        center.add_exit("south", south_loc)
        center.add_exit("east", east_loc)
        center.add_exit("west", west_loc)
        
        # Test north
        player = Player(center)
        result = MoveCommand.execute(player, "n")
        assert result.success is True
        assert player.current_location == north_loc
        
        # Test south
        player = Player(center)
        result = MoveCommand.execute(player, "s")
        assert result.success is True
        assert player.current_location == south_loc
        
        # Test east
        player = Player(center)
        result = MoveCommand.execute(player, "e")
        assert result.success is True
        assert player.current_location == east_loc
        
        # Test west
        player = Player(center)
        result = MoveCommand.execute(player, "w")
        assert result.success is True
        assert player.current_location == west_loc

    def test_invalid_direction(self, player_at_kumeu):
        """Test movement in an invalid direction (no exit)."""
        result = MoveCommand.execute(player_at_kumeu, "east")
        
        assert result.success is False
        assert "cannot" in result.message.lower() or "no exit" in result.message.lower()
        assert player_at_kumeu.current_location.name == "Kumeu"

    def test_invalid_direction_abbreviation(self, player_at_kumeu):
        """Test movement with invalid direction abbreviation."""
        result = MoveCommand.execute(player_at_kumeu, "e")
        
        assert result.success is False
        assert player_at_kumeu.current_location.name == "Kumeu"

    def test_unrecognized_command(self, player_at_kumeu):
        """Test movement with unrecognized command."""
        result = MoveCommand.execute(player_at_kumeu, "invalid")
        
        assert result.success is False
        assert "cannot" in result.message.lower() or "invalid" in result.message.lower()

    def test_case_insensitive_direction(self, player_at_kumeu, setup_locations):
        """Test that direction commands are case-insensitive."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "NORTH")
        
        assert result.success is True
        assert player_at_kumeu.current_location == huapai

    def test_case_insensitive_abbreviation(self, player_at_kumeu, setup_locations):
        """Test that abbreviations are case-insensitive."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "N")
        
        assert result.success is True
        assert player_at_kumeu.current_location == huapai

    def test_movement_result_structure(self, player_at_kumeu):
        """Test that MovementResult has correct structure."""
        result = MoveCommand.execute(player_at_kumeu, "north")
        
        assert hasattr(result, 'success')
        assert hasattr(result, 'message')
        assert isinstance(result.success, bool)
        assert isinstance(result.message, str)

    def test_success_message_contains_location_name(self, player_at_kumeu, setup_locations):
        """Test that success message contains destination location name."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "north")
        
        assert result.success is True
        assert "huapai" in result.message.lower()

    def test_player_location_unchanged_on_failed_move(self, player_at_kumeu):
        """Test that player location doesn't change on failed movement."""
        original_location = player_at_kumeu.current_location
        
        result = MoveCommand.execute(player_at_kumeu, "west")
        
        assert result.success is False
        assert player_at_kumeu.current_location == original_location

    def test_multiple_consecutive_moves(self, setup_locations):
        """Test multiple consecutive movements."""
        kumeu, huapai, _ = setup_locations
        player = Player(kumeu)
        
        # Move north to Huapai
        result1 = MoveCommand.execute(player, "north")
        assert result1.success is True
        assert player.current_location == huapai
        
        # Move south back to Kumeu
        result2 = MoveCommand.execute(player, "south")
        assert result2.success is True
        assert player.current_location == kumeu

    def test_whitespace_handling(self, player_at_kumeu, setup_locations):
        """Test that whitespace in commands is handled properly."""
        kumeu, huapai, _ = setup_locations
        
        result = MoveCommand.execute(player_at_kumeu, "  north  ")
        
        assert result.success is True
        assert player_at_kumeu.current_location == huapai