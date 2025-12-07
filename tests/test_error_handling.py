"""
BDD-style tests for error handling and user feedback feature.

These tests directly match the feature scenarios to ensure proper:
- Success messages for valid actions
- Error messages for invalid inputs
- Case-insensitive command processing
- Whitespace trimming
"""

import pytest
from src.game_engine import GameEngine
from src.location import Location


@pytest.fixture
def game_locations():
    """Create the game world with linked locations."""
    kumeu = Location("Kumeu")
    huapai = Location("Huapai")
    helensville = Location("Helensville")
    riverhead = Location("Riverhead")
    
    # Link locations with exits
    kumeu.add_exit("north", huapai)
    kumeu.add_exit("west", riverhead)
    
    huapai.add_exit("south", kumeu)
    huapai.add_exit("north", helensville)
    
    helensville.add_exit("south", huapai)
    
    riverhead.add_exit("east", kumeu)
    
    return {
        "kumeu": kumeu,
        "huapai": huapai,
        "helensville": helensville,
        "riverhead": riverhead
    }


@pytest.fixture
def game_engine(game_locations):
    """Create a game engine instance starting at Kumeu."""
    return GameEngine(starting_location=game_locations["kumeu"])


class TestErrorHandlingFeature:
    """Test suite for error handling and user feedback feature."""
    
    def test_scenario_1_successful_movement_feedback(self, game_engine):
        """
        Scenario 1: Successful movement with feedback
        
        Given the player is at Kumeu
        When the player moves north
        Then the player should see "You have moved to Huapai"
        And the player's location should be Huapai
        """
        # Given: player is at Kumeu (set up by fixture)
        assert game_engine.current_location.name == "Kumeu"
        
        # When: the player moves north
        result = game_engine.process_command("north")
        
        # Then: appropriate success message and location change
        assert result == "You have moved to Huapai"
        assert game_engine.current_location.name == "Huapai"
    
    def test_scenario_2_invalid_direction_feedback(self, game_engine):
        """
        Scenario 2: Invalid direction error message
        
        Given the player is at Helensville
        When the player tries to move east (invalid exit)
        Then the player should see "You cannot go that way"
        And the player's location should remain Helensville
        """
        # Given: player is at Helensville
        game_engine.process_command("north")  # Move to Huapai
        game_engine.process_command("north")  # Move to Helensville
        assert game_engine.current_location.name == "Helensville"
        
        # When: the player tries to move east
        result = game_engine.process_command("east")
        
        # Then: error message and location unchanged
        assert result == "You cannot go that way"
        assert game_engine.current_location.name == "Helensville"
    
    def test_scenario_3_unrecognized_command_feedback(self, game_engine):
        """
        Scenario 3: Unrecognized command with help suggestion
        
        Given the player is at any location
        When the player enters an unrecognized command "dance"
        Then the player should see error message with help suggestion
        And the player's location should remain unchanged
        """
        # Given: player is at Kumeu
        initial_location = game_engine.current_location.name
        
        # When: the player enters unrecognized command
        result = game_engine.process_command("dance")
        
        # Then: error message with help suggestion
        assert "I don't understand that command" in result
        assert "help" in result.lower()
        assert game_engine.current_location.name == initial_location
    
    def test_scenario_4_case_insensitive_commands(self, game_engine):
        """
        Scenario 4: Case-insensitive command processing
        
        Given the player is at Kumeu
        When the player enters commands in different cases
        Then all variations should work correctly
        """
        # Test uppercase
        result = game_engine.process_command("NORTH")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        # Move back to test mixed case
        game_engine.process_command("south")
        assert game_engine.current_location.name == "Kumeu"
        
        # Test mixed case
        result = game_engine.process_command("North")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        # Move back to test lowercase
        game_engine.process_command("south")
        assert game_engine.current_location.name == "Kumeu"
        
        # Test lowercase
        result = game_engine.process_command("north")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
    
    def test_scenario_5_whitespace_trimming(self, game_engine):
        """
        Scenario 5: Whitespace trimming in command processing
        
        Given the player is at Kumeu
        When the player enters commands with leading/trailing whitespace
        Then the whitespace should be ignored and command processed correctly
        """
        # Test leading whitespace
        result = game_engine.process_command("  north")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        # Move back
        game_engine.process_command("south")
        
        # Test trailing whitespace
        result = game_engine.process_command("north  ")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        # Move back
        game_engine.process_command("south")
        
        # Test both leading and trailing whitespace
        result = game_engine.process_command("  north  ")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        # Move back
        game_engine.process_command("south")
        
        # Test excessive whitespace
        result = game_engine.process_command("    north    ")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
    
    def test_combined_case_and_whitespace(self, game_engine):
        """
        Additional test: Combined case insensitivity and whitespace trimming
        
        Given the player is at Kumeu
        When the player enters commands with both whitespace and different cases
        Then both should be handled correctly
        """
        result = game_engine.process_command("  NORTH  ")
        assert "You have moved to Huapai" == result
        assert game_engine.current_location.name == "Huapai"
        
        result = game_engine.process_command("  SoUtH  ")
        assert "You have moved to Kumeu" == result
        assert game_engine.current_location.name == "Kumeu"
    
    def test_empty_command(self, game_engine):
        """
        Edge case: Empty command handling
        
        Given the player is at any location
        When the player enters an empty command
        Then an appropriate error message should be shown
        """
        initial_location = game_engine.current_location.name
        
        result = game_engine.process_command("")
        
        assert "I don't understand that command" in result or "Please enter a command" in result
        assert game_engine.current_location.name == initial_location
    
    def test_help_command(self, game_engine):
        """
        Feature test: Help command functionality
        
        Given the player is at any location
        When the player enters "help"
        Then help text with available commands should be displayed
        """
        result = game_engine.process_command("help")
        
        assert "help" in result.lower() or "available commands" in result.lower()
        # Help should mention movement commands
        assert any(direction in result.lower() for direction in ["north", "south", "east", "west"])