"""
Integration tests for the movement system.

BDD-style integration tests that map directly to the feature scenarios,
testing the complete movement flow from command to result.
"""

import pytest
from src.location import Location
from src.player import Player
from src.movement import MoveCommand


@pytest.fixture
def test_locations():
    """Create a network of test locations for integration testing."""
    kumeu = Location("Kumeu")
    huapai = Location("Huapai")
    waimauku = Location("Waimauku")
    helensville = Location("Helensville")
    
    # Set up location connections
    kumeu.add_exit("north", huapai)
    kumeu.add_exit("west", waimauku)
    kumeu.add_exit("east", helensville)
    
    huapai.add_exit("south", kumeu)
    huapai.add_exit("east", helensville)
    
    waimauku.add_exit("east", kumeu)
    waimauku.add_exit("north", huapai)
    
    helensville.add_exit("west", kumeu)
    helensville.add_exit("south", waimauku)
    
    return {
        "kumeu": kumeu,
        "huapai": huapai,
        "waimauku": waimauku,
        "helensville": helensville
    }


@pytest.fixture
def player_at_kumeu(test_locations):
    """Create a player starting at Kumeu."""
    return Player(test_locations["kumeu"])


class TestMovementSystemIntegration:
    """Integration tests matching the BDD feature scenarios."""
    
    def test_scenario_1_move_north_successfully(self, test_locations, player_at_kumeu):
        """
        Scenario 1: Successfully moving north
        Given the player is at "Kumeu"
        And there is an exit "north" to "Huapai"
        When the player types "north"
        Then the player should be at "Huapai"
        And the player should see a success message
        """
        # Given
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        huapai = test_locations["huapai"]
        
        assert player.current_location == kumeu
        assert kumeu.get_exit("north") == huapai
        
        # When
        result = MoveCommand.execute(player, "north")
        
        # Then
        assert player.current_location == huapai
        assert result.success is True
        assert "success" in result.message.lower() or "moved" in result.message.lower()
    
    def test_scenario_2_move_west_successfully(self, test_locations, player_at_kumeu):
        """
        Scenario 2: Successfully moving west
        Given the player is at "Kumeu"
        And there is an exit "west" to "Waimauku"
        When the player types "west"
        Then the player should be at "Waimauku"
        And the player should see a success message
        """
        # Given
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        waimauku = test_locations["waimauku"]
        
        assert player.current_location == kumeu
        assert kumeu.get_exit("west") == waimauku
        
        # When
        result = MoveCommand.execute(player, "west")
        
        # Then
        assert player.current_location == waimauku
        assert result.success is True
        assert "success" in result.message.lower() or "moved" in result.message.lower()
    
    def test_scenario_3_invalid_direction(self, test_locations, player_at_kumeu):
        """
        Scenario 3: Attempting to move in an invalid direction
        Given the player is at "Kumeu"
        And there is no exit "south"
        When the player types "south"
        Then the player should remain at "Kumeu"
        And the player should see an error message
        """
        # Given
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        
        assert player.current_location == kumeu
        assert kumeu.get_exit("south") is None
        
        # When
        result = MoveCommand.execute(player, "south")
        
        # Then
        assert player.current_location == kumeu
        assert result.success is False
        assert "error" in result.message.lower() or "cannot" in result.message.lower() or "no exit" in result.message.lower()
    
    def test_scenario_4_abbreviation_support(self, test_locations, player_at_kumeu):
        """
        Scenario 4: Using direction abbreviations
        Given the player is at "Kumeu"
        And there is an exit "east" to "Helensville"
        When the player types "e"
        Then the player should be at "Helensville"
        And the player should see a success message
        """
        # Given
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        helensville = test_locations["helensville"]
        
        assert player.current_location == kumeu
        assert kumeu.get_exit("east") == helensville
        
        # When
        result = MoveCommand.execute(player, "e")
        
        # Then
        assert player.current_location == helensville
        assert result.success is True
        assert "success" in result.message.lower() or "moved" in result.message.lower()
    
    def test_scenario_5_all_cardinal_directions(self, test_locations):
        """
        Scenario 5: Supporting all four cardinal directions
        Given the player is at "Kumeu"
        And there are exits in all four cardinal directions
        When the player moves "north", "south", "east", or "west"
        Then the movement should be processed correctly
        """
        # Given
        kumeu = test_locations["kumeu"]
        huapai = test_locations["huapai"]
        waimauku = test_locations["waimauku"]
        helensville = test_locations["helensville"]
        
        # Test north movement
        player = Player(kumeu)
        result = MoveCommand.execute(player, "north")
        assert result.success is True
        assert player.current_location == huapai
        
        # Test south movement (from Huapai back to Kumeu)
        result = MoveCommand.execute(player, "south")
        assert result.success is True
        assert player.current_location == kumeu
        
        # Test west movement
        player = Player(kumeu)
        result = MoveCommand.execute(player, "west")
        assert result.success is True
        assert player.current_location == waimauku
        
        # Test east movement (from Waimauku to Kumeu)
        result = MoveCommand.execute(player, "east")
        assert result.success is True
        assert player.current_location == kumeu
        
        # Test east movement to Helensville
        result = MoveCommand.execute(player, "east")
        assert result.success is True
        assert player.current_location == helensville
    
    def test_multiple_movements_in_sequence(self, test_locations, player_at_kumeu):
        """
        Additional integration test: Multiple movements in sequence
        Test that the player can make several moves and end up at the correct location.
        """
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        huapai = test_locations["huapai"]
        helensville = test_locations["helensville"]
        waimauku = test_locations["waimauku"]
        
        # Start at Kumeu
        assert player.current_location == kumeu
        
        # Move north to Huapai
        result = MoveCommand.execute(player, "north")
        assert result.success is True
        assert player.current_location == huapai
        
        # Move east to Helensville
        result = MoveCommand.execute(player, "east")
        assert result.success is True
        assert player.current_location == helensville
        
        # Move south to Waimauku
        result = MoveCommand.execute(player, "south")
        assert result.success is True
        assert player.current_location == waimauku
        
        # Move east back to Kumeu
        result = MoveCommand.execute(player, "east")
        assert result.success is True
        assert player.current_location == kumeu
    
    def test_abbreviations_for_all_directions(self, test_locations, player_at_kumeu):
        """
        Additional integration test: All direction abbreviations work
        Test that n, s, e, w abbreviations all work correctly.
        """
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        huapai = test_locations["huapai"]
        waimauku = test_locations["waimauku"]
        helensville = test_locations["helensville"]
        
        # Test 'n' abbreviation
        result = MoveCommand.execute(player, "n")
        assert result.success is True
        assert player.current_location == huapai
        
        # Test 's' abbreviation (back to Kumeu)
        result = MoveCommand.execute(player, "s")
        assert result.success is True
        assert player.current_location == kumeu
        
        # Test 'w' abbreviation
        result = MoveCommand.execute(player, "w")
        assert result.success is True
        assert player.current_location == waimauku
        
        # Test 'e' abbreviation (back to Kumeu)
        result = MoveCommand.execute(player, "e")
        assert result.success is True
        assert player.current_location == kumeu
    
    def test_invalid_direction_does_not_change_location(self, test_locations, player_at_kumeu):
        """
        Additional integration test: Failed movements don't change location
        Ensure that when a move fails, the player stays in the same location.
        """
        player = player_at_kumeu
        kumeu = test_locations["kumeu"]
        
        # Try to move in an invalid direction
        result = MoveCommand.execute(player, "south")
        assert result.success is False
        assert player.current_location == kumeu
        
        # Try another invalid direction
        result = MoveCommand.execute(player, "down")
        assert result.success is False
        assert player.current_location == kumeu
        
        # Verify a valid move still works after failed attempts
        result = MoveCommand.execute(player, "north")
        assert result.success is True
        assert player.current_location == test_locations["huapai"]