"""
Unit tests for Player class.

Tests cover:
- Player initialization
- Current location tracking
- Location updates
"""

import pytest
from src.player import Player
from src.location import Location


class TestPlayerInitialization:
    """Tests for player initialization."""
    
    def test_player_initialized_with_location(self):
        """Test that a player can be initialized with a location."""
        # Given
        location = Location("Kumeu", "A charming rural town")
        
        # When
        player = Player(location)
        
        # Then
        assert player.current_location == location
        assert player.get_current_location() == location
    
    def test_player_stores_location_reference(self):
        """Test that player stores the actual location object."""
        # Given
        location = Location("Helensville", "A historic town")
        
        # When
        player = Player(location)
        
        # Then
        assert player.current_location is location


class TestLocationTracking:
    """Tests for tracking and updating player location."""
    
    def test_get_current_location(self):
        """Test getting the current location."""
        # Given
        location = Location("Parakai", "Known for hot springs")
        player = Player(location)
        
        # When
        current = player.get_current_location()
        
        # Then
        assert current == location
    
    def test_move_to(self):
        """Test moving to a new location."""
        # Given
        kumeu = Location("Kumeu", "A charming rural town")
        huapai = Location("Huapai", "A neighboring village")
        player = Player(kumeu)
        
        # When
        player.move_to(huapai)
        
        # Then
        assert player.current_location == huapai
        assert player.get_current_location() == huapai
    
    def test_location_updates_persist(self):
        """Test that location updates persist across multiple changes."""
        # Given
        location1 = Location("Location1", "First location")
        location2 = Location("Location2", "Second location")
        location3 = Location("Location3", "Third location")
        player = Player(location1)
        
        # When
        player.move_to(location2)
        player.move_to(location3)
        
        # Then
        assert player.get_current_location() == location3
    
    def test_multiple_location_changes(self):
        """Test multiple consecutive location changes."""
        # Given
        locations = [Location(f"Location{i}", f"Description {i}") for i in range(5)]
        player = Player(locations[0])
        
        # When/Then
        for i, location in enumerate(locations):
            if i > 0:
                player.move_to(location)
            assert player.get_current_location() == location


class TestPlayerState:
    """Tests for player state management."""
    
    def test_player_maintains_location_state(self):
        """Test that player maintains location state correctly."""
        # Given
        start_location = Location("Start", "Starting point")
        player = Player(start_location)
        
        # When
        current_before = player.get_current_location()
        new_location = Location("Destination", "Final destination")
        player.move_to(new_location)
        current_after = player.get_current_location()
        
        # Then
        assert current_before == start_location
        assert current_after == new_location
        assert current_before != current_after