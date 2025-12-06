"""Location Display Service for formatting and displaying location information."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.location import Location


class LocationDisplay:
    """Service for formatting and displaying location information."""

    def format_location_info(self, location: 'Location') -> str:
        """
        Format complete location information including name, description, and exits.

        Args:
            location: The Location object to format

        Returns:
            Formatted string with location name, description, and exits
        """
        parts = [
            self.format_name(location),
            self.format_description(location),
            self.format_exits(location)
        ]
        return '\n'.join(parts)

    def format_name(self, location: 'Location') -> str:
        """
        Format the location name.

        Args:
            location: The Location object

        Returns:
            Formatted location name string
        """
        return location.name

    def format_description(self, location: 'Location') -> str:
        """
        Format the location description.

        Args:
            location: The Location object

        Returns:
            Location description string
        """
        return location.description

    def format_exits(self, location: 'Location') -> str:
        """
        Format the available exits for a location.

        Args:
            location: The Location object

        Returns:
            Formatted exits string, or "no obvious exits" if none exist
        """
        if not location.has_exits():
            return "There are no obvious exits."

        exits = location.get_exits()
        if len(exits) == 1:
            return f"There is an exit to the {exits[0]}."
        
        # Multiple exits - format as comma-separated list
        formatted_exits = ', '.join(exits)
        return f"There are exits to the {formatted_exits}."