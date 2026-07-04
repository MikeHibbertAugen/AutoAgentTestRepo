"""
Game world package initialization.

This package provides core game world components for a text-based adventure game
set in north-west Auckland.
"""

try:
    # ``location`` lives under ``src/`` in this repo layout, so this relative
    # import only resolves when the package is installed/laid out that way.
    # Guard it so merely importing this package (e.g. during pytest collection)
    # never hard-fails.
    from .location import Location  # noqa: F401
except ImportError:  # pragma: no cover
    Location = None  # type: ignore[assignment, misc]

__all__ = ['Location']

__version__ = '0.1.0'