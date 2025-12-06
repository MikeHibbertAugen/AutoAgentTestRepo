"""Game controller module for handling game commands and coordinating game state."""

from src.location import Location
from src.player import Player
from src.location_display import LocationDisplay


class GameController:
    """Controller class to handle game commands and coordinate game state."""

    def __init__(self, player: Player, locations: dict[str, Location]):
        """
        Initialize the GameController.

        Args:
            player: Player instance
            locations: Dictionary mapping location names to Location objects
        """
        self.player = player
        self.locations = locations
        self.display = LocationDisplay()

    def handle_look_command(self) -> str:
        """
        Handle the look command to display current location information.

        Returns:
            Formatted string containing location name, description, and exits
        """
        current_location = self.player.get_current_location()
        return self.display.format_location_info(current_location)

    def handle_move_command(self, destination_name: str) -> str:
        """
        Handle movement command to move player to a new location.

        Args:
            destination_name: Name of the destination location

        Returns:
            Formatted string containing new location information after movement
        """
        if destination_name in self.locations:
            new_location = self.locations[destination_name]
            self.player.move_to(new_location)
            return self.display.format_location_info(new_location)
        else:
            return f"Cannot move to '{destination_name}': location not found"

    def look_around(self) -> str:
        """
        Display current location information (alias for handle_look_command).

        Returns:
            Formatted string containing location name, description, and exits
        """
        return self.handle_look_command()