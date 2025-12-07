"""
BDD-style acceptance tests for the Location Description System.

These tests verify the complete feature scenarios for displaying location
information in the text-based adventure game.
"""

import pytest
from src.location import Location
from src.location_display import LocationDisplay
from src.player import Player
from src.game_controller import GameController


class TestLocationDescriptionFeature:
    """BDD acceptance tests matching the feature file scenarios."""

    @pytest.fixture
    def town_square(self):
        """Create the Town Square location with exits."""
        return Location(
            name="Town Square",
            description="A bustling town square filled with merchants and travelers.",
            exits={"north": "Castle Gate", "east": "Market Street"}
        )

    @pytest.fixture
    def castle_gate(self):
        """Create the Castle Gate location."""
        return Location(
            name="Castle Gate",
            description="An imposing gate leading to the castle.",
            exits={"south": "Town Square"}
        )

    @pytest.fixture
    def dark_cave(self):
        """Create the Dark Cave location with no exits."""
        return Location(
            name="Dark Cave",
            description="A dark and mysterious cave.",
            exits={}
        )

    @pytest.fixture
    def locations(self, town_square, castle_gate, dark_cave):
        """Create a dictionary of all locations."""
        return {
            "Town Square": town_square,
            "Castle Gate": castle_gate,
            "Dark Cave": dark_cave
        }

    @pytest.fixture
    def player(self, town_square):
        """Create a player starting at Town Square."""
        return Player(starting_location=town_square)

    @pytest.fixture
    def game_controller(self, player, locations):
        """Create a game controller with player and locations."""
        return GameController(player=player, locations=locations)

    def test_scenario_1_display_location_name_and_description(self, game_controller, town_square):
        """
        Scenario: Display location name and description
        Given I am at "Town Square"
        When I look around
        Then I should see "Town Square"
        And I should see "A bustling town square filled with merchants and travelers."
        """
        # Given: player is at Town Square (set up in fixture)
        assert game_controller.player.get_current_location() == town_square

        # When: I look around
        output = game_controller.look_around()

        # Then: I should see the location name and description
        assert "Town Square" in output
        assert "A bustling town square filled with merchants and travelers." in output

    def test_scenario_2_display_available_exits(self, game_controller, town_square):
        """
        Scenario: Display available exits
        Given I am at "Town Square"
        When I look around
        Then I should see "Exits: north, east"
        """
        # Given: player is at Town Square (set up in fixture)
        assert game_controller.player.get_current_location() == town_square

        # When: I look around
        output = game_controller.look_around()

        # Then: I should see the available exits
        assert "Exits:" in output
        # Check that both directions are present
        assert "north" in output
        assert "east" in output

    def test_scenario_3_automatic_display_on_arrival(self, game_controller, castle_gate, locations):
        """
        Scenario: Automatic display on arrival
        Given I am at "Town Square"
        When I move to "Castle Gate"
        Then I should automatically see "Castle Gate"
        And I should see "An imposing gate leading to the castle."
        And I should see "Exits: south"
        """
        # Given: player is at Town Square (set up in fixture)
        # When: I move to Castle Gate
        output = game_controller.handle_move_command("Castle Gate")

        # Then: I should automatically see the location information
        assert "Castle Gate" in output
        assert "An imposing gate leading to the castle." in output
        assert "Exits:" in output
        assert "south" in output

    def test_scenario_4_explicit_look_command(self, game_controller):
        """
        Scenario: Explicit look command
        Given I am at "Town Square"
        When I use the "look" command
        Then I should see "Town Square"
        And I should see "A bustling town square filled with merchants and travelers."
        And I should see "Exits: north, east"
        """
        # Given: player is at Town Square (set up in fixture)
        # When: I use the look command
        output = game_controller.handle_look_command()

        # Then: I should see complete location information
        assert "Town Square" in output
        assert "A bustling town square filled with merchants and travelers." in output
        assert "Exits:" in output
        assert "north" in output
        assert "east" in output

    def test_scenario_5_location_with_no_exits(self, player, locations, dark_cave):
        """
        Scenario: Location with no exits
        Given I am at "Dark Cave"
        When I look around
        Then I should see "Dark Cave"
        And I should see "A dark and mysterious cave."
        And I should see "There are no obvious exits."
        """
        # Given: player is at Dark Cave
        player.move_to(dark_cave)
        game_controller = GameController(player=player, locations=locations)

        # When: I look around
        output = game_controller.look_around()

        # Then: I should see location info with no exits message
        assert "Dark Cave" in output
        assert "A dark and mysterious cave." in output
        assert "There are no obvious exits." in output


class TestLocationDescriptionEdgeCases:
    """Additional edge case tests for the location description system."""

    def test_location_with_single_exit(self):
        """Test formatting for a location with a single exit."""
        location = Location(
            name="Narrow Passage",
            description="A narrow passage between rocks.",
            exits={"west": "Town Square"}
        )
        player = Player(starting_location=location)
        game_controller = GameController(
            player=player,
            locations={"Narrow Passage": location, "Town Square": location}
        )

        output = game_controller.look_around()

        assert "Narrow Passage" in output
        assert "A narrow passage between rocks." in output
        assert "west" in output

    def test_location_with_multiple_exits(self):
        """Test formatting for a location with multiple exits."""
        location = Location(
            name="Crossroads",
            description="A crossroads with paths in all directions.",
            exits={
                "north": "Forest",
                "south": "Town",
                "east": "Mountains",
                "west": "River"
            }
        )
        player = Player(starting_location=location)
        game_controller = GameController(
            player=player,
            locations={"Crossroads": location}
        )

        output = game_controller.look_around()

        assert "Crossroads" in output
        assert "A crossroads with paths in all directions." in output
        assert "north" in output
        assert "south" in output
        assert "east" in output
        assert "west" in output

    def test_move_and_look_consistency(self):
        """Test that move and look commands show the same information."""
        start = Location(
            name="Start",
            description="Starting location.",
            exits={"east": "End"}
        )
        end = Location(
            name="End",
            description="Ending location.",
            exits={"west": "Start"}
        )
        locations = {"Start": start, "End": end}
        player = Player(starting_location=start)
        game_controller = GameController(player=player, locations=locations)

        # Move to End location
        move_output = game_controller.handle_move_command("End")

        # Look at End location
        look_output = game_controller.handle_look_command()

        # Both should contain the same location information
        assert "End" in move_output
        assert "End" in look_output
        assert "Ending location." in move_output
        assert "Ending location." in look_output