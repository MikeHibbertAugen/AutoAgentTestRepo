"""
Unit tests for GameState class.

This module contains comprehensive unit tests for the GameState class,
testing initialization, state transitions, and location management.
"""

import pytest
from src.game_state import GameState


class TestGameStateInitialization:
    """Test GameState initialization."""

    def test_game_state_initializes_with_default_values(self):
        """Test that GameState initializes with correct default values."""
        game_state = GameState()
        
        assert game_state.is_running is False
        assert game_state.get_current_location() is not None

    def test_game_state_initializes_with_starting_location(self):
        """Test that GameState initializes with a starting location."""
        game_state = GameState()
        
        location = game_state.get_current_location()
        assert isinstance(location, str)
        assert len(location) > 0


class TestGameStateRunningStatus:
    """Test GameState running status management."""

    def test_start_sets_is_running_to_true(self):
        """Test that start() sets is_running to True."""
        game_state = GameState()
        
        game_state.start()
        
        assert game_state.is_running is True

    def test_stop_sets_is_running_to_false(self):
        """Test that stop() sets is_running to False."""
        game_state = GameState()
        game_state.start()
        
        game_state.stop()
        
        assert game_state.is_running is False

    def test_multiple_start_calls_maintain_running_state(self):
        """Test that multiple start() calls maintain running state."""
        game_state = GameState()
        
        game_state.start()
        game_state.start()
        
        assert game_state.is_running is True

    def test_multiple_stop_calls_maintain_stopped_state(self):
        """Test that multiple stop() calls maintain stopped state."""
        game_state = GameState()
        game_state.start()
        
        game_state.stop()
        game_state.stop()
        
        assert game_state.is_running is False


class TestGameStateLocationManagement:
    """Test GameState location management."""

    def test_get_current_location_returns_string(self):
        """Test that get_current_location() returns a string."""
        game_state = GameState()
        
        location = game_state.get_current_location()
        
        assert isinstance(location, str)

    def test_set_current_location_updates_location(self):
        """Test that set_current_location() updates the current location."""
        game_state = GameState()
        new_location = "You are in a dark forest."
        
        game_state.set_current_location(new_location)
        
        assert game_state.get_current_location() == new_location

    def test_set_current_location_accepts_different_descriptions(self):
        """Test that set_current_location() accepts various location descriptions."""
        game_state = GameState()
        locations = [
            "You are in a bright meadow.",
            "You are standing at a crossroads.",
            "You are in a dimly lit cave.",
        ]
        
        for location in locations:
            game_state.set_current_location(location)
            assert game_state.get_current_location() == location

    def test_location_persists_across_state_changes(self):
        """Test that location persists when game state changes."""
        game_state = GameState()
        location = "You are in a magical castle."
        
        game_state.set_current_location(location)
        game_state.start()
        assert game_state.get_current_location() == location
        
        game_state.stop()
        assert game_state.get_current_location() == location


class TestGameStateTransitions:
    """Test GameState state transitions."""

    def test_state_transition_from_stopped_to_running(self):
        """Test state transition from stopped to running."""
        game_state = GameState()
        assert game_state.is_running is False
        
        game_state.start()
        
        assert game_state.is_running is True

    def test_state_transition_from_running_to_stopped(self):
        """Test state transition from running to stopped."""
        game_state = GameState()
        game_state.start()
        assert game_state.is_running is True
        
        game_state.stop()
        
        assert game_state.is_running is False

    def test_state_transitions_do_not_affect_location(self):
        """Test that state transitions do not modify location."""
        game_state = GameState()
        initial_location = game_state.get_current_location()
        
        game_state.start()
        assert game_state.get_current_location() == initial_location
        
        game_state.stop()
        assert game_state.get_current_location() == initial_location


class TestGameStateTypeCorrectness:
    """Test GameState type correctness."""

    def test_is_running_returns_boolean(self):
        """Test that is_running is a boolean."""
        game_state = GameState()
        
        assert isinstance(game_state.is_running, bool)
        
        game_state.start()
        assert isinstance(game_state.is_running, bool)

    def test_get_current_location_returns_string_type(self):
        """Test that get_current_location() always returns string type."""
        game_state = GameState()
        
        location = game_state.get_current_location()
        assert isinstance(location, str)
        
        game_state.set_current_location("New location")
        location = game_state.get_current_location()
        assert isinstance(location, str)

    def test_set_current_location_accepts_string_parameter(self):
        """Test that set_current_location() properly handles string parameter."""
        game_state = GameState()
        test_location = "Test location string"
        
        game_state.set_current_location(test_location)
        
        assert game_state.get_current_location() == test_location
        assert isinstance(game_state.get_current_location(), str)