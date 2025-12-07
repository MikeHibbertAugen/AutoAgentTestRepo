"""
Unit tests for feedback messages module.

Tests message formatting functions, message constant definitions,
and parameterized message generation.
"""

import pytest
from src.feedback_messages import (
    get_movement_success_message,
    get_invalid_direction_message,
    get_unrecognized_command_message,
    HELP_SUGGESTION,
    AVAILABLE_COMMANDS,
)


class TestMovementSuccessMessages:
    """Tests for successful movement feedback messages."""

    def test_movement_success_message_format(self):
        """Test that movement success message contains location name."""
        location_name = "Huapai"
        message = get_movement_success_message(location_name)
        
        assert location_name in message
        assert len(message) > 0
        assert isinstance(message, str)

    def test_movement_success_message_different_locations(self):
        """Test movement messages for various locations."""
        locations = ["Huapai", "Kumeu", "Helensville", "Riverhead"]
        
        for location in locations:
            message = get_movement_success_message(location)
            assert location in message
            assert message != get_movement_success_message("Different Place")


class TestInvalidDirectionMessages:
    """Tests for invalid direction error messages."""

    def test_invalid_direction_message_format(self):
        """Test that invalid direction message is informative."""
        direction = "west"
        message = get_invalid_direction_message(direction)
        
        assert len(message) > 0
        assert isinstance(message, str)
        assert direction in message.lower() or "that direction" in message.lower()

    def test_invalid_direction_message_different_directions(self):
        """Test invalid direction messages for various directions."""
        directions = ["north", "south", "east", "west"]
        
        for direction in directions:
            message = get_invalid_direction_message(direction)
            assert len(message) > 0


class TestUnrecognizedCommandMessages:
    """Tests for unrecognized command error messages."""

    def test_unrecognized_command_message_format(self):
        """Test that unrecognized command message contains command."""
        command = "dance"
        message = get_unrecognized_command_message(command)
        
        assert len(message) > 0
        assert isinstance(message, str)
        assert command in message.lower() or "command" in message.lower()

    def test_unrecognized_command_message_includes_help(self):
        """Test that unrecognized command message suggests help."""
        message = get_unrecognized_command_message("invalid")
        
        assert "help" in message.lower()


class TestHelpMessages:
    """Tests for help and suggestion messages."""

    def test_help_suggestion_exists(self):
        """Test that help suggestion constant is defined."""
        assert HELP_SUGGESTION is not None
        assert len(HELP_SUGGESTION) > 0
        assert isinstance(HELP_SUGGESTION, str)
        assert "help" in HELP_SUGGESTION.lower()

    def test_available_commands_exists(self):
        """Test that available commands list is defined."""
        assert AVAILABLE_COMMANDS is not None
        assert len(AVAILABLE_COMMANDS) > 0
        assert isinstance(AVAILABLE_COMMANDS, str)


class TestMessageConsistency:
    """Tests for message consistency and format standards."""

    def test_messages_are_not_empty(self):
        """Test that all message functions return non-empty strings."""
        assert len(get_movement_success_message("TestLocation")) > 0
        assert len(get_invalid_direction_message("north")) > 0
        assert len(get_unrecognized_command_message("test")) > 0

    def test_messages_are_strings(self):
        """Test that all message functions return string types."""
        assert isinstance(get_movement_success_message("TestLocation"), str)
        assert isinstance(get_invalid_direction_message("north"), str)
        assert isinstance(get_unrecognized_command_message("test"), str)

    def test_messages_are_user_friendly(self):
        """Test that messages don't contain technical jargon or error codes."""
        messages = [
            get_movement_success_message("Huapai"),
            get_invalid_direction_message("west"),
            get_unrecognized_command_message("dance"),
        ]
        
        technical_terms = ["exception", "error code", "null", "undefined", "traceback"]
        
        for message in messages:
            for term in technical_terms:
                assert term not in message.lower()