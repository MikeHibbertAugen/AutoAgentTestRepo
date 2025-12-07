"""
Unit tests for the HelpSystem class.

This module contains comprehensive tests for the help system functionality,
including help text generation, welcome message display, and command coverage.
"""

import pytest
from src.help_system import HelpSystem


@pytest.fixture
def help_system():
    """
    Fixture that provides a HelpSystem instance for testing.
    
    Returns:
        HelpSystem: A fresh HelpSystem instance for each test.
    """
    return HelpSystem()


class TestHelpSystemInstantiation:
    """Tests for HelpSystem instantiation."""
    
    def test_help_system_instantiation(self):
        """Test that HelpSystem can be instantiated successfully."""
        system = HelpSystem()
        assert system is not None
        assert isinstance(system, HelpSystem)


class TestGetHelpText:
    """Tests for the get_help_text method."""
    
    def test_get_help_text_returns_non_empty_string(self, help_system):
        """Test that get_help_text returns a non-empty string."""
        help_text = help_system.get_help_text()
        assert isinstance(help_text, str)
        assert len(help_text) > 0
    
    def test_help_text_contains_north_command(self, help_system):
        """Test that help text contains the 'north' movement command."""
        help_text = help_system.get_help_text()
        assert "north" in help_text.lower()
    
    def test_help_text_contains_south_command(self, help_system):
        """Test that help text contains the 'south' movement command."""
        help_text = help_system.get_help_text()
        assert "south" in help_text.lower()
    
    def test_help_text_contains_east_command(self, help_system):
        """Test that help text contains the 'east' movement command."""
        help_text = help_system.get_help_text()
        assert "east" in help_text.lower()
    
    def test_help_text_contains_west_command(self, help_system):
        """Test that help text contains the 'west' movement command."""
        help_text = help_system.get_help_text()
        assert "west" in help_text.lower()
    
    def test_help_text_contains_north_abbreviation(self, help_system):
        """Test that help text contains the 'n' abbreviation for north."""
        help_text = help_system.get_help_text()
        assert "n" in help_text.lower()
    
    def test_help_text_contains_south_abbreviation(self, help_system):
        """Test that help text contains the 's' abbreviation for south."""
        help_text = help_system.get_help_text()
        assert "s" in help_text.lower()
    
    def test_help_text_contains_east_abbreviation(self, help_system):
        """Test that help text contains the 'e' abbreviation for east."""
        help_text = help_system.get_help_text()
        assert "e" in help_text.lower()
    
    def test_help_text_contains_west_abbreviation(self, help_system):
        """Test that help text contains the 'w' abbreviation for west."""
        help_text = help_system.get_help_text()
        assert "w" in help_text.lower()
    
    def test_help_text_contains_look_command(self, help_system):
        """Test that help text contains the 'look' utility command."""
        help_text = help_system.get_help_text()
        assert "look" in help_text.lower()
    
    def test_help_text_contains_help_command(self, help_system):
        """Test that help text contains the 'help' utility command."""
        help_text = help_system.get_help_text()
        assert "help" in help_text.lower()
    
    def test_help_text_contains_quit_command(self, help_system):
        """Test that help text contains the 'quit' utility command."""
        help_text = help_system.get_help_text()
        assert "quit" in help_text.lower()
    
    def test_help_text_contains_all_movement_commands(self, help_system):
        """Test that help text contains all movement commands."""
        help_text = help_system.get_help_text().lower()
        movement_commands = ["north", "south", "east", "west"]
        for command in movement_commands:
            assert command in help_text
    
    def test_help_text_contains_all_utility_commands(self, help_system):
        """Test that help text contains all utility commands."""
        help_text = help_system.get_help_text().lower()
        utility_commands = ["look", "help", "quit"]
        for command in utility_commands:
            assert command in help_text


class TestGetWelcomeMessage:
    """Tests for the get_welcome_message method."""
    
    def test_get_welcome_message_returns_non_empty_string(self, help_system):
        """Test that get_welcome_message returns a non-empty string."""
        welcome_message = help_system.get_welcome_message()
        assert isinstance(welcome_message, str)
        assert len(welcome_message) > 0
    
    def test_welcome_message_contains_help_hint(self, help_system):
        """Test that welcome message includes hint to type 'help'."""
        welcome_message = help_system.get_welcome_message().lower()
        assert "help" in welcome_message
    
    def test_welcome_message_is_welcoming(self, help_system):
        """Test that welcome message contains welcoming text."""
        welcome_message = help_system.get_welcome_message().lower()
        welcoming_words = ["welcome", "start", "begin", "adventure", "game"]
        assert any(word in welcome_message for word in welcoming_words)
    
    def test_welcome_message_different_from_help_text(self, help_system):
        """Test that welcome message is different from help text."""
        welcome_message = help_system.get_welcome_message()
        help_text = help_system.get_help_text()
        assert welcome_message != help_text


class TestHelpSystemFormatting:
    """Tests for help text formatting and structure."""
    
    def test_help_text_is_readable(self, help_system):
        """Test that help text contains line breaks for readability."""
        help_text = help_system.get_help_text()
        assert "\n" in help_text
    
    def test_welcome_message_formatting(self, help_system):
        """Test that welcome message is properly formatted."""
        welcome_message = help_system.get_welcome_message()
        # Should be a reasonable length
        assert len(welcome_message) < 1000
        # Should contain some structure
        assert len(welcome_message.split()) > 5